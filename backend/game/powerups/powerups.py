import json
import sys
import os
sys.path.append(os.path.abspath('../../aws'))

from sqs import receive_messages_from_SQS, delete_messages_from_SQS
from constants import SQS_POWERUPS_QUEUE_URL
from freeze import activate_Freeze
from multiplier import activate_Multiplier

def check_for_powerup_purchases( ):
    # Read from the SQS for power ups
    messages = receive_messages_from_SQS(SQS_POWERUPS_QUEUE_URL)

    if (not messages):
        return False

    receiptHandlesSet = set()
    receiptHandles = []

    for message in messages:

        # Handle deleting the messages
        id = message['MessageId']
        receiptHandle = message['ReceiptHandle']
        if(id in receiptHandlesSet):
            continue
        receiptHandlesSet.add(id)
        receiptHandles.append({
            'Id': id,
            'ReceiptHandle': receiptHandle
        })

        try:
            body = json.loads(message['Body'])
            username = body['username']
            powerUpType = body['powerUpType']
            quantity = body['quantity']
        except Exception as err:
            print("Invalid Bosy")
            continue

        # Power Up types
        if(powerUpType == "FREEZE"):
            activate_Freeze(username, quantity)
        elif(powerUpType == "MULTIPLIER"):
            activate_Multiplier(username, quantity)
        elif(powerUpType == "EXTENDER"):
            pass
        else:
            print('Invalid Power Up Type')

    # Delete messages
    try:
        delete_messages_from_SQS( receiptHandles, SQS_POWERUPS_QUEUE_URL )
    except Exception as err:
        print('Error deleting message', err)
