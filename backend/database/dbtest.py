import json
import boto3
import random

def add(rds_client, username=random.randint(1000000,9999999)):
    return rds_client.execute_statement(
        continueAfterTimeout = True,
        resourceArn = 'INSERT DB ARN',
        secretArn = 'INSERT DB SECRET ARN',
        database = 'users',
        sql = 'INSERT INTO ButtonParty (username, score) VALUES (:new_username, :new_score)',
        parameters = [
            {'name': 'new_username', 'value': {'stringValue': str(username)}}, 
            {'name': 'new_score', 'value': {'longValue': 0}}
            ]
        )

client = boto3.client('rds-data', region_name='us-east-1')

if __name__ == "__main__":
    add(client)
