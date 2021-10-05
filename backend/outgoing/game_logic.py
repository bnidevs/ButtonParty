import sys
import os
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../incoming'))
import random
import time
import json

from constants import BUTTON_FREQUENCY, SQS_SCORING_QUEUE_URL
from rds import get_user_from_RDS, update_user_in_RDS
from sqs import receive_messages_from_SQS, delete_messages_from_SQS
from helper import validateJson

def run_button_game():
    while(True):
        time.sleep(1)
        if( random.random() < 1 / BUTTON_FREQUENCY ):
            print('Sending out SNS notification')
            send_message_to_SNS('PRESS BUTTON')

def increment_score(username, streak):
    try:
        user = get_user_from_RDS( username )
    except Exception as err:
        print('Unable to get User', err)
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
    messages = remove_duplicates(receive_messages_from_SQS( SQS_SCORING_QUEUE_URL ))
    if(len(messages) == 0):
        return False
    receiptHandles = []
    for message in messages:
        receiptHandles.append({
            'Id': message['MessageId'],
            'ReceiptHandle': message['ReceiptHandle']
        })
        try:
            body = json.loads(message['Body'])
        except Exception as err:
            body = None
        if(validateJson(body)):
            increment_score( body['username'], body['streak']);
    delete_messages_from_SQS( receiptHandles, SQS_SCORING_QUEUE_URL )
    return True
