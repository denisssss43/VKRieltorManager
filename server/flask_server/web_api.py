from server.flask_server import web_app
from flask import request, render_template

import json
import sys

# from vk_parser.lib.cfg.cfg import *
# import vk_parser.lib.db_post as db_post

# @app.route('/api/')

@web_app.route('/api')
@web_app.route('/api/')
def api(): 

	result = db_post.Execute(db_post.Connect(), 
	"""
	SELECT * FROM post_library.post;
	""")

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