import sys
import os
sys.path.append(os.path.abspath('../'))

from constants import SNS_ARN, SNS_CLIENT

def send_message_to_SNS( message ):
    SNS_CLIENT.publish(
        TargetArn=SNS_ARN,
        Message=message
    )
