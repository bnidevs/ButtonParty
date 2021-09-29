import sys
import os
sys.path.append(os.path.abspath('../'))
import json
import random

def add_user_to_RDS(rds_client, username=random.randint(1000000,9999999)):
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
