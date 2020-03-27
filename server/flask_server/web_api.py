from flask import request, render_template

import json
import sys

from server.flask_server import web_app
import server._lib.db_post as db_post
from server._lib.cfg.cfg import *

@web_app.route('/api')
@web_app.route('/api/')
def api(): 

	result = db_post.Execute(
		db_post.Connect(), 
		"""SELECT * FROM post_library.telephone;""")

	return json.dumps(result, indent=4)

@web_app.route('/api/post/')
def post(): 
	
	offset = 0

	result = db_post.Execute(
		db_post.Connect(), 
		"""SELECT * FROM post_library.telephone ORDER BY id LIMIT 10 OFFSET {0};""".format(offset))

	return json.dumps(result, indent=4)

@web_app.route('/api/vinegret')
def api_GetVinegret(): 
	# products = [
	#     {'id':'0','title':'что-то','title':'что-то','title':'что-то',},
	#     {'id':'1','title':'что-то','title':'что-то','title':'что-то',},
	#     {'id':'2','title':'что-то','title':'что-то','title':'что-то',},
	#     {'id':'3','title':'что-то','title':'что-то','title':'что-то',},
	# ]

	# result = db_post.Execute(db_post.Connect(), 
	# """
	# SELECT * FROM post_library.post;
	# """)

	# return json.dumps(result, indent=4)

	return 'Молодец, да это web-api'