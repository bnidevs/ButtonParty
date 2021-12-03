import json
import sys
import os
sys.path.append(os.path.abspath('../'))

from constants import SQS_INCOMING_QUEUE_URL, REGION, SQS_CLIENT
from rds import add_user_to_RDS
from sns import add_platform_app_endpoint, subscribe_endpoint_to_topic

def delete_messages_from_SQS( receipt_handle, QUEUE_URL ):
    # Delete received message from queue
    SQS_CLIENT.delete_message_batch(
        QueueUrl=QUEUE_URL,
        Entries=receipt_handle
    )

def purge_queue_from_SQS ( QUEUE_URL ):
    SQS_CLIENT.purge_queue(
        QueueUrl=QUEUE_URL
    )

def send_message_to_SQS( message, QUEUE_URL ):
    SQS_CLIENT.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=message
    )

def receive_messages_from_SQS( QUEUE_URL ):
    # Receive message from SQS queue
    response = SQS_CLIENT.receive_message(
        QueueUrl=QUEUE_URL,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=1,
        WaitTimeSeconds= 3
    )

    if('Messages' in response):
        return response['Messages']
    return False

def add_new_users():
    # Read up to 10 messages
    messages = receive_messages_from_SQS( SQS_INCOMING_QUEUE_URL )

    if(not messages):
        return False

    receiptHandles = []
    receiptHandlesSet = set()
    for message in messages:

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
            token = body['token']
        except Exception as err:
            print(err)
            continue

        try:
            add_user_to_RDS(username)
            subscribe_endpoint_to_topic( add_platform_app_endpoint(token) )
        except Exception as err:
            print(f'Unable to add user: {username}\n', err)

    # Delete messages
    try:
        delete_messages_from_SQS( receiptHandles, SQS_INCOMING_QUEUE_URL )
    except Exception as err:
        print('Error deleting message', err)

    return True
