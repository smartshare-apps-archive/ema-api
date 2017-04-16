import sqlite3


def getRedisConfig(config_db):
	q = """SELECT value FROM settings WHERE name="RedisConfig";"""

	try:
		config_db.execute(q)
	except Exception as e:
		print "Unable to find redis configuration settings: ", e
		return None

	redis_config = config_db.fetchone()

	if redis_config:
		redis_config = filter(lambda i: i != '', redis_config[0].split('<redis_split>'))

		formattedRedisConfig = {}
		for setting in redis_config:
			setting = setting.split('=')
			formattedRedisConfig[setting[0]] = setting[1]

		return formattedRedisConfig




def getDatabaseConfig(config_db):
	q = """SELECT value FROM settings WHERE name="DatabaseConfig";"""

	try:
		config_db.execute(q)
	except Exception as e:
		print "Unable to find database configuration settings: ", e
		return None

	database_config = config_db.fetchone()
	
	if database_config:
		database_config = filter(lambda i: i != '', database_config[0].split('<database_split>'))

		formattedDatabaseConfig = {}
		for setting in database_config:
			setting = setting.split('=')
			formattedDatabaseConfig[setting[0]] = setting[1]

		return formattedDatabaseConfig



def getRecordCount(ema_db):
	q = """SELECT COUNT(*) FROM erpubtbl;"""
	try:
		ema_db.execute(q)
	except Exception as e:
		print "Error getting record count: ", e
		return None

	count = ema_db.fetchone()
	if count:
		return count[0]