import redis
import tokenize

from database.db import *
from uuid import uuid4


def connect_cache(redis_config):	
	try:
		r = redis.StrictRedis(host=redis_config["host"],port=redis_config["port"], password=redis_config["password"])
	except Exception as e:
		print "Error connecting to redis cache:", e
		return None

	return r


def grab_records(ema_db, start_index, end_index):
	q = "SELECT Title, pmid FROM erpubtbl LIMIT %s,%s;"

	try:
		ema_db.execute(q, (start_index, end_index, ))
	except Exception as e:
		print "Error getting records: ", e
		return None

	records = ema_db.fetchall()

	if records:
		for record in records:
			print record




def main():
	config_db = config_handle()
	redis_config = config.getRedisConfig(config_db.cursor())

	r = connect_cache(redis_config)

	print "Connected to redis:", r.ping()

	ema_db = db_handle(config_db)
	records = grab_records(ema_db.cursor(), 0, 1000)



	ema_db.close()
	config_db.close()


if __name__ == "__main__":main()