from __future__ import print_function 
import os, sys, re, time, json

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, url_for, abort, request, Response, make_response, g, current_app, session


#api endpoints
from api import search_actions
from database.db import *


application = Flask(__name__)


#jinja2 configuration options
application.jinja_env.trim_blocks = True
application.jinja_env.lstrip_blocks = True


#generate a random secret key
application.secret_key = os.urandom(24)

#register blueprints
application.register_blueprint(search_actions.searchActions)





@application.route('/')
def index():
	return render_template("base.html")






#only for debugging, makes sure to check all the js files and templates for changes
def debug_dirUpdate():
	extra_dirs = ['templates/','static/js/']
	extra_files = extra_dirs[:]
	for extra_dir in extra_dirs:
	    for dirname, dirs, files in os.walk(extra_dir):
	        for filename in files:
	            filename = os.path.join(dirname, filename)
	            if os.path.isfile(filename):
	                extra_files.append(filename)
	return extra_files




if __name__ == "__main__":
	extra_files = debug_dirUpdate()

	#live_host = "0.0.0.0"
	live_host = "127.0.0.1"


	application.run(host = live_host, debug=True, extra_files=extra_files, threaded=True)