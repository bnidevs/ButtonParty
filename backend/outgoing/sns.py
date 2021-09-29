import sys
import os
sys.path.append(os.path.abspath('../'))
import random
import time

from constants import SNS_ARN, SNS_CLIENT, BUTTON_FREQUENCY

def run_button_game():
    while(True):
        time.sleep(1)
        if( random.random() < 1 / BUTTON_FREQUENCY ):
            print('Sending out SNS notification')
            send_message_to_SNS('PRESS BUTTON')

def send_message_to_SNS( message ):
    SNS_CLIENT.publish(
        TargetArn=SNS_ARN,
        Message=message
    )

if __name__ == '__main__':
    run_button_game()
