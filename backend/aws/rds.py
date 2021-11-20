import sys
import os
sys.path.append(os.path.abspath('../'))
import json
import random

from constants import RDS_CLIENT, RDS_RESOURCE_ARN, RDS_SECRET_ARN, DATABASE_NAME
from sql import SET_LATE_USERS_STREAK_TO_ZERO_SQL, GET_MULTIPLER_OF_USER, GET_EXTENDER_OF_USER

def rds_execute_statement( sql, parameters ):
    return RDS_CLIENT.execute_statement(
        continueAfterTimeout = True,
        resourceArn = RDS_RESOURCE_ARN,
        secretArn = RDS_SECRET_ARN,
        database = DATABASE_NAME,
        sql = sql,
        parameters = parameters
        )

def set_late_users_streak_to_zero():
    return rds_execute_statement( SET_LATE_USERS_STREAK_TO_ZERO_SQL, [])

def set_pressed_to_false_for_all():
    sql = 'UPDATE ButtonParty SET pressed = False'
    return rds_execute_statement( sql, [] )

def add_user_to_RDS(username=random.randint(1000000,9999999)):

    # Main Table
    sql = 'INSERT INTO ButtonParty (username, score, streak) VALUES (:new_username, :new_score, :new_streak)'
    parameters = [
        {'name': 'new_username', 'value': {'stringValue': str(username)}},
        {'name': 'new_score', 'value': {'longValue': 0}},
        {'name': 'new_streak', 'value': {'longValue': 0}}
    ]
    rds_execute_statement(sql, parameters)

    # Freeze table
    sql = 'INSERT INTO FreezePowerUp VALUES(:new_username, NULL)'
    rds_execute_statement(sql, parameters)

    # Multiplier Table
    sql = 'INSERT INTO MultiplierPowerUp VALUES(:new_username, NULL, 1)'
    rds_execute_statement(sql, parameters)

    # Extender Table
    sql = 'INSERT INTO ExtenderPowerUp VALUES(:new_username, NULL, 1)'
    rds_execute_statement(sql, parameters)

def get_user_from_RDS(username):
    sql = 'SELECT * FROM ButtonParty WHERE username=:input_username;'
    parameters = [
        {'name': 'input_username', 'value': {'stringValue': str(username)}}
    ]
    response = rds_execute_statement(sql, parameters)['records'][0]
    return {
        'username': response[0]['stringValue'],
        'score': response[1]['longValue'],
        'streak': response[2]['longValue'],
        'pressed': response[3]['booleanValue']
    }

def update_user_in_RDS(username, score, streak):
    sql = 'UPDATE ButtonParty SET score=:new_score, streak=:new_streak, pressed = True WHERE username=:input_username;'
    parameters = [
        {'name': 'input_username', 'value': {'stringValue': str(username)}},
        {'name': 'new_score', 'value': {'longValue': score}},
        {'name': 'new_streak', 'value': {'longValue': streak}}
    ]
    return rds_execute_statement(sql, parameters)

def get_multiplier_of_user(username):
    parameters = [
        {'name': 'input_username', 'value': {'stringValue': str(username)}}
    ]
    response = rds_execute_statement(GET_MULTIPLER_OF_USER, parameters)['records']
    if(response):
        return response[0][0]['longValue']
    else:
        return 1

def get_extender_of_user( username ):
    parameters = [
        {'name': 'input_username', 'value': {'stringValue': str(username)}}
    ]
    response = rds_execute_statement(GET_EXTENDER_OF_USER, parameters)['records']
    if(response):
        return response[0][0]['doubleValue']
    else:
        return 1

# Table updates
def rds_update_freezer_table(username, sqlStatement):
    parameters = parameters = [
        {'name': 'input_username', 'value': {'stringValue': str(username)}}
        ]
    return rds_execute_statement(sqlStatement, parameters)

def rds_update_multiplier_table(username, multiplier, sqlStatement):
    parameters = [
        {'name': 'input_username', 'value': {'stringValue': str(username)}},
        {'name': 'input_multiplier', 'value': {'longValue': multiplier}}
        ]
    return rds_execute_statement( sqlStatement, parameters)

def rds_update_extender_table(username, multiplier, sqlStatement):
    parameters = [
        {'name': 'input_username', 'value': {'stringValue': str(username)}},
        {'name': 'input_multiplier', 'value': {'doubleValue': multiplier}}
        ]
    return rds_execute_statement( sqlStatement, parameters )
