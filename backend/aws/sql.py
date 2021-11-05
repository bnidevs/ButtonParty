
# Set the User's steak to zero if too late
# Also if the user has a freeze activated, don't reset the streak
SET_LATE_USERS_STREAK_TO_ZERO_SQL = '''
UPDATE
	ButtonParty
SET
	streak = 0
WHERE
	pressed = false
    and username NOT IN (	SELECT FreezePowerUp.username
							FROM FreezePowerUp
                            WHERE
								username = FreezePowerUp.username
                                and NOW() <= FreezePowerUp.activeUntil )
;
'''

ADD_USER_TO_RDS_SQL = '''
INSERT INTO ButtonParty (username, score, streak) VALUES (:new_username, :new_score, :new_streak);
INSERT INTO FreezePowerUp VALUES(:new_username, 0, 0, 0, 0, NULL);
'''
