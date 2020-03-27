import uuid, pymysql, ast, copy
from datetime import datetime, timedelta
from contextlib import closing
from pymysql.cursors import DictCursor

from server._lib.cfg.cfg import Config

# NOTE:Изменено и откомментировано полностью
def Connect():
	"""Подключение к БД"""
	cfg = Config() # Объявление обработчика конфигурационного файла

	try: # Попытка подключения к БД по параметрам из конфигурационного файла
		print(
			"""pymysql.connect(\n\thost={0},\n\tuser={1},\n\tpassword={2},\n\tdb={3},\n\tcharset={4},\n\tcursorclass=DictCursor,\n\tconnect_timeout={5})
			""".format(cfg.post_library_host, cfg.post_library_user, cfg.post_library_password, cfg.post_library_db, 'utf8', .4))
		result = pymysql.connect(
			host=cfg.post_library_host, 
			user=cfg.post_library_user, 
			password=cfg.post_library_password, 
			db=cfg.post_library_db, 
			charset='utf8', 
			cursorclass=DictCursor, 
			connect_timeout=.4)
		return result
	except: pass

	
	try:  # Попытка подключения к БД по параметрам из конфигурационного файла, но по локальному адресу
		print(
			"""pymysql.connect(\n\thost={0},\n\tuser={1},\n\tpassword={2},\n\tdb={3},\n\tcharset={4},\n\tcursorclass=DictCursor,\n\tconnect_timeout={5})
			""".format('localhost', cfg.post_library_user, cfg.post_library_password, cfg.post_library_db, 'utf8', .4))
		result = pymysql.connect(
			host='localhost', 
			user=cfg.post_library_user, 
			password=cfg.post_library_password, 
			db=cfg.post_library_db, 
			charset='utf8', 
			cursorclass=DictCursor, 
			connect_timeout=.4)
		return result
	except: pass
	
	print ('pymysql.connect None') 
	return None

# NOTE:Изменено и откомментировано полностью
def CloseConnect(connection):
	"""Закрытие подключения к БД"""
	if connection != None: connection.close()


def GetCountry(connection, uuid=''):
	"""Получение страны по uuid (post_library)"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute(
				"""
				SELECT * 
				FROM post_library.country 
				WHERE uuid='{0}';
				""".format(str(uuid)))
			return cursor.fetchone()
	return None

def GetCity(connection, uuid=''):
	"""Получение города по uuid (post_library)"""
	
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute(
				"""
				SELECT * 
				FROM post_library.city 
				WHERE uuid='{0}';
				""".format(str(uuid)))
			return cursor.fetchone()
	return None

def GetCommunity(connection):
	"""Получение списка групп, по которым необходимо собирать информацию (post_library)"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute(
				"""
				SELECT 
					`id`, 
					`uuid`, 
					`uuid_city`, 
					(SELECT `title` FROM post_library.city LIMIT 1) as city, 
					`url` 
				FROM post_library.community;
				""")
			return cursor.fetchall()
	return None

def AddCommunity(connection, countryTitle='', cityTitle='', communityURL=''):
	"""Добавление сообщества в БД post_library"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			print(
				"""call post_library.sp_addCommunity(\n\t'{0}',\n\t'{1}',\n\t'{2}');
				""".format(str(countryTitle),str(cityTitle),str(communityURL)))
			cursor.execute(
				"""
				call post_library.sp_addCommunity(
					'{0}', 
					'{1}', 
					'{2}');
				""".format(str(countryTitle),str(cityTitle),str(communityURL)))
			connection.commit()
	pass

def AddPost(connection, communityURL='', description='', dateTime=datetime.now(), price=0.0, url='', telephones=[]):
	"""Добавление поста в БД (post_library)"""
	result = {'uuid':None, 'status':None}
	
	if price <= 0: return result

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute(
				"""
				call post_library.sp_addPost(
					'{0}',
					'{1}',
					'{2}',
					{3},
					'{4}');
				""".format(communityURL, description[:1024], str(dateTime), str(price), url))
			result = cursor.fetchone()
			for num in telephones:
				AddTelephone(
					connection, 
					result['uuid'], 
					str(num))
			connection.commit()
	return result

def AddTelephone(connection, uuid_post='',telephone=''):
	"""Добавление телефона в БД (post_library)"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute(
				"""
				call post_library.sp_addTelephone(
					'{0}', 
					'{1}');
				""".format(uuid_post, telephone))
			connection.commit()
	pass

def AddAddress(connection, uuid_post='', countryTitle='', cityTitle='', addressTitle='', latitude=0.0, longitude=0.0):
	"""Добавление адреса в БД (post_library)"""

	if connection != None: # Если подключение создано
		addressTitle = str(addressTitle) if addressTitle=='NULL' else ("'"+str(addressTitle)+"'")
		with connection.cursor() as cursor:
			cursor.execute(
				"""
				call post_library.sp_addAddress(
					'{0}', 
					'{1}', 
					'{2}', 
					{3}, 
					{4}, 
					{5});
				""".format(uuid_post, countryTitle, cityTitle, addressTitle, str(latitude), str(longitude)))
			connection.commit()
	pass

def AddImg(connection, uuid_post='', _img_url=''):
	"""Добавление изображения в БД (post_library)"""
	# print ("uuid post:{0} img url:{1}".format(uuid_post,_img_url))
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute(
				"""
				call post_library.sp_addImg(
					'{0}', 
					'{1}');
				""".format(uuid_post, _img_url))
			connection.commit()
	pass


def Execute(connection, sql):
	result = None
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			print(sql)
			cursor.execute(sql)
			result = cursor.fetchall()
			connection.commit()
	else: return result
	return result
