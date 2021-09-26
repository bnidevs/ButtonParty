import json
import boto3

from constants import QUEUE_URL, REGION, RDS_CLIENT, SQS_CLIENT
from rds import add_user_to_RDS

def delete_messages_from_SQS( receipt_handle ):
    # Delete received message from queue
    SQS_CLIENT.delete_message_batch(
        QueueUrl=QUEUE_URL,
        Entries=receipt_handle
    )

def receive_messages_from_SQS():
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
        VisibilityTimeout=10,
        WaitTimeSeconds= 3
    )

    if('Messages' in response):
        return response['Messages']
    return False

def add_new_users():
    # Read up to 10 messages
    messages = receive_messages_from_SQS()

    if(not messages):
        return False

    receiptHandles = []
    receiptHandlesSet = set()
    for message in messages:
        username = message['Body']
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
            add_user_to_RDS(RDS_CLIENT, username)
        except Exception as err:
            print(f'Unable to add user: {username}\n', err)

    # Delete messages
    try:
        delete_messages_from_SQS( receiptHandles )
    except Exception as err:
        print('Error deleting message', err)

    return True


if __name__ == '__main__':

    while(add_new_users()):
        pass
