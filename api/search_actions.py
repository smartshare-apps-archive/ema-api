import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request, g

from cache import index
from cache import search
from cache import tokenize

from cache.main import *

searchActions = Blueprint('searchActions', __name__, template_folder='templates')



@searchActions.before_request
def setup_session():
	pass


def pull_records(pmids, ema_db):
	placeholders = ','.join(['%s' for _ in pmids])
	q = "SELECT title FROM erpubtbl WHERE pmid IN(%s);" % placeholders
	#print q
	try:
		ema_db.execute(q, pmids)
	except Exception as e:
		print "Error retreiving titles:", e
		return None

	titles = ema_db.fetchall()

	if titles:
		#print titles
		return list(titles)


@searchActions.route('/search/title', methods=['POST'])
##@admin_required(current_app, session, login_redirect)
def search_by_title():
	searchTerm = request.form['searchTerm']
	searchTerm = json.loads(searchTerm)

	config_db = config_handle()
	redis_config = config.getRedisConfig(config_db.cursor())

	r = connect_cache(redis_config)			#grab a connection to the redis cache
	ema_db = db_handle(config_db)		#grab connection handle to the ema db


	search_result = search.parse_and_search(r, searchTerm)

	
	
	print "result: ", search_result

	if search_result == None:
		return json.dumps({"no_results": None})

	cardinality = r.scard('idx:' + search_result)


	if cardinality > 0:
		set_members = list(r.smembers('idx:' + search_result))

		titles = pull_records(set_members, ema_db.cursor())
		#full_results = zip(titles, set_members)
		#print len(titles), len(set_members)
		#print type(cardinality), ":", type(set_members)
		
		
		ema_db.close()
		return json.dumps({"search_results": titles})
		
	else:

		ema_db.close()
		return json.dumps({"no_results": None})




