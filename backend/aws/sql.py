
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

GET_MULTIPLER_OF_USER = '''
SELECT
	multiplier
FROM
	MultiplierPowerUp
WHERE
	activeUntil >= NOW()
	and username = :input_username
;
'''
