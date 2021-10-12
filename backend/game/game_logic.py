import sys
import os
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../aws'))
import random
import time
import json

from constants import BUTTON_FREQUENCY, TIME_TO_PRESS, SQS_SCORING_QUEUE_URL, SQS_TIMESTAMP_QUEUE_URL
from rds import get_user_from_RDS, update_user_in_RDS
from sqs import receive_messages_from_SQS, delete_messages_from_SQS, purge_queue_from_SQS, send_message_to_SQS, add_new_users
from sns import send_message_to_SNS
from helper import validateJson

timestamp_button_limit = None

def call_events():
    print('Button Activated')
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
    if(time_passed >= TIME_TO_PRESS):
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

def is_valid_timestamp( timestamp_from_request ):
    timestamp = get_timestamp()
    user_time_to_press = (timestamp_from_request - timestamp) / 1000
    if( user_time_to_press <= TIME_TO_PRESS ):
        return True
    return False

def increment_score(username, streak, player_timestamp):
    try:
        user = get_user_from_RDS( username )
    except Exception as err:
        print('Unable to get User', err)
        return

    if( not is_valid_timestamp( player_timestamp )):
        print('Button pressed after acceptable time limit')
        return

    # If the streak, is zero, no points are added No need to check for cheating
    if( streak == 0):
        try:
            update_user_in_RDS( username=user['username'], score=user['score'], streak=0 )
        except Exception as err:
            print('Unable to update RDS', err)
        return

    # Make sure the streak is only 1 more than what is stored in the DB
    if ( user['streak'] + 1 == streak ):
        if(streak <= 10):
            new_score = user['score'] + streak
        else:
            new_score =  user['score'] + (streak * streak)

        try:
            update_user_in_RDS( username=user['username'], score=new_score, streak=streak )
        except Exception as err:
            print('Unable to update RDS', err)

    # Something had gone wrong, likely frontent manipulation
    else:
        expected = user['streak']
        print(f'Streak not what expected: expected:{ expected } got:{streak}')

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
        try:
            body = json.loads(message['Body'])
        except Exception as err:
            body = None
        if(validateJson(body)):
            increment_score( body['username'], body['streak'], player_timestamp);
    delete_messages_from_SQS( receiptHandles, SQS_SCORING_QUEUE_URL )
    return True

if __name__ == '__main__':
    print("1 - Checking for new Users")
    print("2 - Run check for pressed button")
    print("3 - Run the random button press")
    print("4 - Force Button press")
    num = int(input("Input 1-4: "))
    if( num == 1 ):
        while(True):
            add_new_users()
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
