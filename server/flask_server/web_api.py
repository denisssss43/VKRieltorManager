from flask import request, render_template

import json
import sys

from server.flask_server import web_app
import server._lib.db_post as db_post
from server._lib.cfg.cfg import *


# Веб апи: 
# 1.	Посты (/api/post?txt=txt&tel=+79834564566&cty=Красноярск&ctry=Россия&offset=0). Сортировка по новым.
# 2.	3

# format = request.args.get('format')
@web_app.route('/api/post')
def	post():
	text = request.args.get('txt')
	telephone = request.args.get('tel')
	city = request.args.get('cty')
	country = request.args.get('ctry')
	

	offset = 0
	try: offset = int(request.args.get('offset'))
	finally: pass

	print (text, telephone, city, country, offset)

	result = db_post.Execute(
		db_post.Connect(), 
		"""
		SELECT description, price, num_telephone, title_country, title_city, title_address, latitude, longitude, url_img
		FROM post_library.v_post_lite 
		WHERE 	description LIKE '{0}' or 
				-- '{0}' LIKE description or
				num_telephone = '{1}' or 
				title_city = '{2}' or 
				title_country = '{3}'

		LIMIT 10 OFFSET {4};""".format(
			text,
			telephone,
			city,
			country,
			offset))


	return json.dumps(result, indent=4)





# @web_app.route('/api')
# @web_app.route('/api/')
# def api(): 

# 	result = db_post.Execute(
# 		db_post.Connect(), 
# 		"""SELECT * FROM post_library.telephone;""")

# 	return json.dumps(result, indent=4)

# @web_app.route('/api/post/')
# def post(): 
	
# 	offset = 0

# 	result = db_post.Execute(
# 		db_post.Connect(), 
# 		"""SELECT * FROM post_library.telephone ORDER BY id LIMIT 10 OFFSET {0};""".format(offset))

# 	return json.dumps(result, indent=4)

# @web_app.route('/api/vinegret')
# def api_GetVinegret(): 
# 	# products = [
# 	#     {'id':'0','title':'что-то','title':'что-то','title':'что-то',},
# 	#     {'id':'1','title':'что-то','title':'что-то','title':'что-то',},
# 	#     {'id':'2','title':'что-то','title':'что-то','title':'что-то',},
# 	#     {'id':'3','title':'что-то','title':'что-то','title':'что-то',},
# 	# ]

# 	# result = db_post.Execute(db_post.Connect(), 
# 	# """
# 	# SELECT * FROM post_library.post;
# 	# """)

# 	# return json.dumps(result, indent=4)

# 	return 'Молодец, да это web-api'