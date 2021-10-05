import sys
import os
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../incoming'))
import random
import time

from rds import get_user_from_RDS, update_user_in_RDS

def increment_score(username, streak):

    try:
        user = get_user_from_RDS( username )
    except Exception as err:
        print('Unable to get User', err)
        return

    # If the streak, is zero, no points are added No need to check for cheating
    if( streak == 0):
        try:
            update_user_in_RDS( username=user['username'], score=user['score'], streak=0 )
        except Exception as err:
            print('Unable to update RDS', err)
        return

    # Make sure the streak is only 1 more than what is stored in the DB
    if ( user['streak'] + 1 == streak ):
        if(streak <= 10):
            new_score = user['score'] + streak
        else:
            new_score =  user['score'] + (streak * streak)

        try:
            update_user_in_RDS( username=user['username'], score=new_score, streak=streak )
        except Exception as err:
            print('Unable to update RDS', err)

    # Something had gone wrong, likely frontent manipulation
    else:
        expected = user['streak']
        print(f'Streak not what expected: expected:{ expected } got:{streak}')

increment_score('apinkow27', 11)
