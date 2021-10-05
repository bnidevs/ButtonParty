'''
File contains constants that are used
'''
from boto3 import client

# URL of the SQS queue ButtonParty-Incoming
QUEUE_URL = 'INSERT SQS_QUEUE URL'

# AWS Region
REGION = 'us-east-1'

# RDS Client
RDS_CLIENT = client('rds-data', region_name=REGION)

# SQS Client
SQS_CLIENT = client('sqs', region_name=REGION)
