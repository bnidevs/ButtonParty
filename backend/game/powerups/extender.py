import sys
import os
sys.path.append(os.path.abspath('../../aws'))
sys.path.append(os.path.abspath('../../'))

from rds import get_user_from_RDS, update_user_in_RDS, rds_update_multiplier_table

sql = '''
UPDATE ExtenderPowerUp
SET activeUntil = ADDTIME(NOW(), '06:00:00'), multiplier = :input_multiplier
WHERE username = :input_username
;
'''

PRICE_1Halfx_EXTENDER = 60
PRICE_2x_EXTENDER = 150
PRICE_3x_EXTENDER = 330
PRICE_5x_EXTENDER = 700

priceOfExtender = {
    2: PRICE_1Halfx_EXTENDER,
    3: PRICE_2x_EXTENDER,
    5: PRICE_3x_EXTENDER,
    10: PRICE_5x_EXTENDER
}

def activate_Extender(username, multiplier):
    # Make sure there is a valid multiplier
    if(multiplier not in priceOfMultiplier):
        return

    # Get the user information
    rdsUser = get_user_from_RDS(username)
    score = rdsUser['score']
    streak = rdsUser['streak']

    # Check to make sure they have enough points
    if( score < priceOfMultiplier[multiplier] ):
        return

    # Activate the Multiplier
    rds_update_multiplier_table( username, multiplier, sql )

    # Remove the points
    update_user_in_RDS(username, score-priceOfMultiplier[multiplier], streak)
