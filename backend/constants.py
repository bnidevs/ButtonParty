'''
File contains constants that are used
'''
from boto3 import client

# Button frequency : 1/ BUTTON_FREQUENCY
BUTTON_FREQUENCY = 10000

# URL of the SQS queue ButtonParty-Incoming
SQS_INCOMING_QUEUE_URL = 'INSERT SQS_QUEUE URL'

# URL of the SQS queue ButtonParty-Scoring
SQS_SCORING_QUEUE_URL = 'arn:aws:sqs:us-east-1:291201070981:ButtonParty-Scoring'

# AWS Region
REGION = 'us-east-1'

# RDS DATABASE name
DATABASE_NAME = 'users'

# RDS_RESOURCE_ARN
RDS_RESOURCE_ARN = '***REMOVED***'

# RDS SECRET ARN
RDS_SECRET_ARN = '***REMOVED***'

# SNS ARN
SNS_ARN = 'INSERT SNS ARN'

# RDS Client
RDS_CLIENT = client('rds-data', region_name=REGION)

# SQS Client
SQS_CLIENT = client('sqs', region_name=REGION)

# SNS CLIENT
SNS_CLIENT = client('sns', region_name=REGION)
