import sys
import os
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../aws'))
sys.path.append(os.path.abspath('./powerups'))
import random
import time
import json

from constants import BUTTON_FREQUENCY, TIME_TO_PRESS, SQS_SCORING_QUEUE_URL, SQS_TIMESTAMP_QUEUE_URL
from rds import get_user_from_RDS, update_user_in_RDS, set_late_users_streak_to_zero, set_pressed_to_false_for_all, get_multiplier_of_user, get_extender_of_user
from sqs import receive_messages_from_SQS, delete_messages_from_SQS, purge_queue_from_SQS, send_message_to_SQS, add_new_users
from powerups import check_for_powerup_purchases
from sns import send_message_to_SNS
from helper import validateJson

MAX_EXTENDER_PERIOD = 5
timestamp_button_limit = None

def call_events():
    print('Button Activated')
    # Extra Catch to make sure the streaks are set to 0
    set_late_users_streak_to_zero()
    # Set Pressed for all users
    set_pressed_to_false_for_all()
    # Clear out the SQS TIMESTAMP QUEUE
    purge_queue_from_SQS( SQS_TIMESTAMP_QUEUE_URL )
    # Send out a message to the SQS TIMESTAMP DATABASE
    send_message_to_SQS( 'PRESS BUTTON', SQS_TIMESTAMP_QUEUE_URL )
    # Send out push notification to users
    send_message_to_SNS('PRESS BUTTON')

def run_button_game():
    while(True):
        time.sleep(1)
        if( random.random() < 1 / BUTTON_FREQUENCY ):
            call_events()
            time.sleep(60)

def reset_timestamp():
    global timestamp_button_limit
    if(timestamp_button_limit == None):
        return
    now = time.time() * 1000
    time_passed = ( now - timestamp_button_limit ) / 1000
    if(time_passed >= TIME_TO_PRESS * MAX_EXTENDER_PERIOD):
        timestamp_button_limit = None

def get_timestamp():
    global timestamp_button_limit
    if(timestamp_button_limit == None):
        try:
            message = receive_messages_from_SQS( SQS_TIMESTAMP_QUEUE_URL )[0]
            timestamp_button_limit = int(message['Attributes']['SentTimestamp'])
        except Exception as err:
            timestamp_button_limit = None
    return timestamp_button_limit

def is_valid_timestamp( timestamp_from_request, extender ):
    timestamp = get_timestamp()
    user_time_to_press = (timestamp_from_request - timestamp) / 1000
    if( user_time_to_press <= TIME_TO_PRESS * extender ):
        return True
    return False

def increment_score(username, player_timestamp):
    try:
        user = get_user_from_RDS( username )
        multiplier = get_multiplier_of_user( username )
        extender = get_extender_of_user( username )
    except Exception as err:
        print('Unable to get User', err)
        return

    if( not is_valid_timestamp( player_timestamp, extender )):
        print('TIME LIMIT EXCEEDED')
        return

    if( user['pressed'] ):
        print(f"USER {user['username']} already pressed button")
        return

    streak = user['streak'] + 1
    if(streak <= 10):
        new_score = user['score'] + streak * multiplier
    else:
        new_score =  user['score'] + (streak * streak) * multiplier

    try:
        update_user_in_RDS( username=user['username'], score=new_score, streak=streak )
    except Exception as err:
        print('Unable to update RDS', err)

    print(f"User {username} successfully pressed the button")

def remove_duplicates(messages):
    if(not messages):
        return []
    r = []
    ids = set()
    for message in messages:
        if( message['MessageId'] in ids):
            continue
        r.append(message)
        ids.add(message['MessageId'])
    return r

def check_the_pressed_buttons():
    reset_timestamp()
    messages = remove_duplicates(receive_messages_from_SQS( SQS_SCORING_QUEUE_URL ))
    if(len(messages) == 0):
        return False
    receiptHandles = []
    for message in messages:
        receiptHandles.append({
            'Id': message['MessageId'],
            'ReceiptHandle': message['ReceiptHandle']
        })
        player_timestamp = int(message['Attributes']['SentTimestamp'])
        body = json.loads(message['Body'])
        username = body['username']
        increment_score( username, player_timestamp );
    delete_messages_from_SQS( receiptHandles, SQS_SCORING_QUEUE_URL )
    return True

if __name__ == '__main__':
    print("1 - Check for all 3 SQS requests (users, presses, powerups)")
    print("2 - Run check for pressed button")
    print("3 - Run the random button press")
    print("4 - Force Button press")
    num = int(input("Input 1-4: "))
    if( num == 1 ):
        while(True):
            add_new_users()
            check_the_pressed_buttons()
            check_for_powerup_purchases()
    elif( num == 2 ):
        while(True):
            check_the_pressed_buttons()
    elif( num == 3 ):
        while(True):
            run_button_game();
    elif( num == 4 ):
        call_events()
    else:
        print("Invalid Input")
