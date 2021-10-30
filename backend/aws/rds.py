import sys
import os
sys.path.append(os.path.abspath('../'))
import json
import random

from constants import RDS_CLIENT, RDS_RESOURCE_ARN, RDS_SECRET_ARN, DATABASE_NAME

def set_late_users_streak_to_zero():
    return RDS_CLIENT.execute_statement(
        continueAfterTimeout = True,
        resourceArn = RDS_RESOURCE_ARN,
        secretArn = RDS_SECRET_ARN,
        database = DATABASE_NAME,
        sql = f'Update ButtonParty SET streak = 0 WHERE pressed = False;'
    )

def set_pressed_to_false_for_all():
    return RDS_CLIENT.execute_statement(
        continueAfterTimeout = True,
        resourceArn = RDS_RESOURCE_ARN,
        secretArn = RDS_SECRET_ARN,
        database = DATABASE_NAME,
        sql = 'UPDATE ButtonParty SET pressed = False'
    )

def add_user_to_RDS(username=random.randint(1000000,9999999)):
    return RDS_CLIENT.execute_statement(
        continueAfterTimeout = True,
        resourceArn = RDS_RESOURCE_ARN,
        secretArn = RDS_SECRET_ARN,
        database = DATABASE_NAME,
        sql = 'INSERT INTO ButtonParty (username, score, streak) VALUES (:new_username, :new_score, :new_streak)',
        parameters = [
            {'name': 'new_username', 'value': {'stringValue': str(username)}},
            {'name': 'new_score', 'value': {'longValue': 0}},
            {'name': 'new_streak', 'value': {'longValue': 0}}
            ]
        )

def get_user_from_RDS(username):
    response = RDS_CLIENT.execute_statement(
        continueAfterTimeout = True,
        resourceArn = RDS_RESOURCE_ARN,
        secretArn = RDS_SECRET_ARN,
        database = DATABASE_NAME,
        sql = f'SELECT * FROM ButtonParty WHERE username=:input_username;',
        parameters = [
            {'name': 'input_username', 'value': {'stringValue': str(username)}}
            ]
        )['records'][0]
    return {
        'username': response[0]['stringValue'],
        'score': response[1]['longValue'],
        'streak': response[2]['longValue'],
        'pressed': response[3]['booleanValue']
    }

def update_user_in_RDS(username, score, streak):
    return RDS_CLIENT.execute_statement(
        continueAfterTimeout = True,
        resourceArn = RDS_RESOURCE_ARN,
        secretArn = RDS_SECRET_ARN,
        database = DATABASE_NAME,
        sql = f'UPDATE ButtonParty SET score=:new_score, streak=:new_streak, pressed = True WHERE username=:input_username;',
        parameters = [
            {'name': 'input_username', 'value': {'stringValue': str(username)}},
            {'name': 'new_score', 'value': {'longValue': score}},
            {'name': 'new_streak', 'value': {'longValue': streak}}
            ]
        )