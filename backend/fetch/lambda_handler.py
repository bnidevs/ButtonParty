import json
import boto3

def lambda_handler(event, context):
    
    fetch_type = event['rawPath'].split('/')[-1]
    
    print(fetch_type)
    
    RDS_CLIENT = boto3.client('rds-data', region_name='us-east-1')
    
    if fetch_type == 'self':
        
        username = event['rawQueryString'].split('=')[-1]
        
        print(username)
        
        try:
            response = RDS_CLIENT.execute_statement(
                continueAfterTimeout = True,
                resourceArn = 'INSERT DB CLUSTER ARN HERE',
                secretArn = 'INSERT SECRET ARN HERE',
                database = 'users',
                sql = f'SELECT * FROM ButtonParty WHERE username=:username;',
                parameters = [
                    {'name': 'username', 'value': {'stringValue': str(username)}},
                ]
            )['records'][0]
            
            response = {
                'username': response[0]['stringValue'],
                'score': response[1]['longValue'],
                'streak': response[2]['longValue']
            }
        except Exception as e:
            response = {
                'error': str(e)
            }
            
        print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
