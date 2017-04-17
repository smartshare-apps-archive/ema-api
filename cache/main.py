import redis

import tokenize
import index
import search

from database.db import *


import database.config as config

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
		formattedRecords = {}
		for record in records:
			formattedRecords[record[1]] = record[0]

		return formattedRecords



def create_inverted_index(r, ema_db):
	record_count = config.getRecordCount(ema_db.cursor())
	print "Record count: ", record_count

	records_per_step = 10000

	if populate_cache:
		current_index = 0 
		while(current_index < record_count):
			#print "Current record start index: ", current_index
			records = grab_records(ema_db.cursor(), 0, current_index + records_per_step) #grab some records

			for pmid, title in records.iteritems():
				tokens = tokenize.title(title)

				#print tokens
				clen = index.index_article(r, pmid, tokens)
				#print "Current cache length: ", clen
			
			current_index += records_per_step





def main():
	populate_cache = False

	config_db = config_handle()
	redis_config = config.getRedisConfig(config_db.cursor())

	print "Using the following cache configuration:", redis_config

	r = connect_cache(redis_config)			#grab a connection to the redis cache

	ema_db = db_handle(config_db)		#grab connection handle to the ema db

	if populate_cache:
		create_inverted_index(r, ema_db)


	#check if redis connection was successful
	try:
		r.ping()
	except redis.exceptions.ConnectionError as e:
		print "Could not connect to redis server: ", e
		return False


	

	#test = search.parse_query('A sad big man complex inhibition doctor man is me!')
	search_term = "baseball -blues"
	search_result = search.parse_and_search(r, search_term)

	print r.scard('idx:' + search_result)
	print r.smembers('idx:' + search_result)

	#clean up
	ema_db.close()
	config_db.close()


if __name__ == "__main__":main()