import sys
import os
sys.path.append(os.path.abspath('../'))

from constants import SNS_CLIENT, SNS_PlATFORM_ARN, SNS_TOPIC_ARN

def send_message_to_SNS( message ):
    SNS_CLIENT.publish(
        TargetArn=SNS_TOPIC_ARN,
        Message=message
    )

def add_platform_app_endpoint( token ):
    return SNS_CLIENT.create_platform_endpoint(
        PlatformApplicationArn=SNS_PlATFORM_ARN,
        Token=token
    )['EndpointArn']


def subscribe_endpoint_to_topic( endpoint ):
    return SNS_CLIENT.subscribe(
        TopicArn=SNS_TOPIC_ARN,
        Protocol='application',
        Endpoint=endpoint
    )
