import sys
import os
sys.path.append(os.path.abspath('../../aws'))
sys.path.append(os.path.abspath('../../'))

from rds import get_user_from_RDS, update_user_in_RDS, rds_update_multiplier_table

sql = '''
UPDATE MultiplierPowerUp
SET activeUntil = ADDTIME(NOW(), '06:00:00'), multiplier = :input_multiplier
WHERE username = :input_username
;
'''

PRICE_2x_MULTIPLIER = 60
PRICE_3x_MULTIPLIER = 150
PRICE_5x_MULTIPLIER = 330
PRICE_10x_MULTIPLIER = 700

priceOfMultiplier = {
    2: PRICE_2x_MULTIPLIER,
    3: PRICE_3x_MULTIPLIER,
    5: PRICE_5x_MULTIPLIER,
    10: PRICE_10x_MULTIPLIER
}

def activate_Multiplier(username, multiplier):
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
