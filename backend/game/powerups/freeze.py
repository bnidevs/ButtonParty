import sys
import os
sys.path.append(os.path.abspath('../../aws'))
sys.path.append(os.path.abspath('../../'))

from rds import get_user_from_RDS, rds_update_freezer_table, update_user_in_RDS

ACTIVATE_FREEZE_SQL = f'UPDATE FreezePowerUp SET activeUntil = (SELECT ADDTIME(NOW(), \'REPLACE\')) WHERE username = :input_username;'

PRICE_6_HOURS = 60
PRICE_12_HOURS = 150
PRICE_24_HOURS = 330
PRICE_48_HOURS = 700

priceOfFreeze = {
    6: PRICE_6_HOURS,
    12: PRICE_12_HOURS,
    24: PRICE_24_HOURS,
    48: PRICE_48_HOURS
}

timeOfFreeze = {
    6: '06:00:00',
    12: '12:00:00',
    24: '24:00:00',
    48: '48:00:00'
}

def activate_Freeze( username, duration ):
    # Make sure there is a valid duration
    if(duration not in priceOfFreeze):
        return

    # Get the user information
    rdsUser = get_user_from_RDS(username)
    score = rdsUser['score']
    streak = rdsUser['streak']

    # Check to make sure they have enough points
    # Return if you do not have enough points
    if(score < priceOfFreeze[duration] ):
        return

    # Activate the Freeze
    rds_update_freezer_table( username, ACTIVATE_FREEZE_SQL.replace('REPLACE', timeOfFreeze[duration]) )

    # Remove the points
    update_user_in_RDS(username, score-priceOfFreeze[duration], streak)

# print(ACTIVATE_FREEZE_SQL.replace('REPLACE', timeOfFreeze[6]))
activate_Freeze('apinkow27', 6)
