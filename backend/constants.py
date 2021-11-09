'''
File contains constants that are used
'''
from boto3 import client

# Button frequency : 1/ BUTTON_FREQUENCY
BUTTON_FREQUENCY = 10000

# In case of delay, we give a small buffer to the time to press
TIME_TO_PRESS_BUFFER = 10

# The user has the press the button within a certain amount of time
TIME_TO_PRESS = 100 + TIME_TO_PRESS_BUFFER

# URL of the SQS queue ButtonParty-Incoming
SQS_INCOMING_QUEUE_URL = 'REPLACE'

# URL of the SQS queue ButtonParty-Scoring
SQS_SCORING_QUEUE_URL = 'REPLACE'

# URL of the SQS ButtonParty-check_timestamp
SQS_TIMESTAMP_QUEUE_URL = 'REPLACE'

# AWS Region
REGION = 'us-east-1'

# RDS DATABASE name
DATABASE_NAME = 'users'

# RDS_RESOURCE_ARN
RDS_RESOURCE_ARN = 'REPLACE'

# RDS SECRET ARN
RDS_SECRET_ARN = 'REPLACE'

# SNS Platform Application
SNS_PlATFORM_ARN = 'REPLACE'

# SNS Topic Arn
SNS_TOPIC_ARN = 'REPLACE'

# RDS Client
RDS_CLIENT = client('rds-data', region_name=REGION)

# SQS Client
SQS_CLIENT = client('sqs', region_name=REGION)

# SNS CLIENT
SNS_CLIENT = client('sns', region_name=REGION)
