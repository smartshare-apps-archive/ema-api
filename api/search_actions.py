import json, ast, re

from flask import Blueprint, render_template, abort, current_app, session, request


searchActions = Blueprint('searchActions', __name__, template_folder='templates')



@searchActions.before_request
def setup_session():
	pass




@searchActions.route('/search/title', methods=['POST'])
##@admin_required(current_app, session, login_redirect)
def search_by_title():
	pass




