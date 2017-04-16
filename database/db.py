"""
this just provides helper functions to grab handles to the rds database as well the configuration database, which stores database server settings,
as well as the config for the redis server
"""

import sqlite3
import MySQLdb

import config 	#config is mostly get/set routines to pull various settings from the local config db

CONFIG_DB = "database/config.db"


#grab connection handle to the local config db (sqlite3)
def config_handle():	
	try:
		conn=sqlite3.connect(CONFIG_DB)
		conn.text_factory = str
		
	except Exception as e:
		print "Error opening instance database: ", e
		return None
	
	return conn



#grab connection handle to the foreign ema db (mysql)
def db_handle(config_db):
	db_settings = config.getDatabaseConfig(config_db.cursor())
	print "Using the following remote database configuration:", db_settings

	try:
		conn=MySQLdb.connect(host=db_settings["host"],port=int(db_settings["port"]),user=db_settings["username"],passwd=db_settings["password"], db=db_settings["default_db"], use_unicode=True, charset="utf8", connect_timeout=1)
	except Exception as e:
		print "Exception connecting: ", e
		return None
	return conn




def main():
	config_db = config_handle()
	redis_config = config.getRedisConfig(config_db.cursor())

	ema_db = db_handle(config_db)

	ema_db.close()
	config_db.close()



if __name__ == "__main__":main()