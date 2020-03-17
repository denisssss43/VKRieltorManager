import uuid
from datetime import datetime, timedelta
import pymysql
from contextlib import closing
from pymysql.cursors import DictCursor
import ast 
import copy

from vk_parser.lib.cfg.cfg import Config

connection = None # Объект подключения к бд 

# NOTE:Изменено и откомментировано полностью
def Connect():
	"""Подключение к БД"""
	global connection

	cfg = Config()

	try: 
		connection = pymysql.connect(
			host=cfg.post_library_host, 
			user=cfg.post_library_user, 
			password=cfg.post_library_password, 
			db=cfg.post_library_db, 
			charset='utf8', 
			cursorclass=DictCursor, 
			connect_timeout=.4)
	except: 
		connection = pymysql.connect(
			host='localhost', 
			user=cfg.post_library_user, 
			password=cfg.post_library_password, 
			db=cfg.post_library_db, 
			charset='utf8', 
			cursorclass=DictCursor, 
			connect_timeout=.4)
# NOTE:Изменено и откомментировано полностью
def CloseConnect():
	"""Закрытие подключения к БД"""
	global connection
	if connection != None: 
		connection.close()
		connection = None


def GetCountry(uuid=''):
	"""Получение страны по uuid (post_library)"""
	result = None
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM post_library.country WHERE uuid='"+str(uuid)+"';")
			result = cursor.fetchone()
	return result

def GetCity(uuid=''):
	"""Получение города по uuid (post_library)"""
	result = None
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM post_library.city WHERE uuid='"+str(uuid)+"';")
			result = cursor.fetchone()
	return result

def GetCommunity():
	"""Получение списка групп, по которым необходимо собирать информацию (post_library)"""
	result = None
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("""
				SELECT 
					`id`, 
					`uuid`, 
					`uuid_city`, 
					(SELECT `title` FROM post_library.city LIMIT 1) as city, 
					`url` 
				FROM post_library.community;
				""")
			result = cursor.fetchall()
	return result

def AddCommunity(countryTitle='', cityTitle='', communityURL=''):
	"""Добавление сообщества в БД post_library"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call post_library.sp_addCommunity('"+str(countryTitle)+"', '"+str(cityTitle)+"', '"+str(communityURL)+"');")
			connection.commit()
	pass

def AddPost(communityURL='', description='', dateTime=datetime.now(), price=0.0, url='', telephones=[]):
	"""Добавление поста в БД (post_library)"""
	result = {'uuid':'', 'status':0}
	
	if price <= 0: return result

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call post_library.sp_addPost('"+str(communityURL)+"','"+str(description)[:1024]+"','"+str(dateTime)+"',"+str(price)+",'"+str(url)+"');")
			result = cursor.fetchone()
			for num in telephones:
				AddTelephone(result['uuid'], str(num))
			connection.commit()

	return result

def AddTelephone(uuid_post='',telephone=''):
	"""Добавление телефона в БД (post_library)"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call post_library.sp_addTelephone('"+str(uuid_post)+"', '"+str(telephone)+"');")
			connection.commit()
	pass

def AddAddress(uuid_post='', countryTitle='', cityTitle='', addressTitle='', latitude=0.0, longitude=0.0):
	"""Добавление адреса в БД (post_library)"""

	if connection != None: # Если подключение создано
		addressTitle = str(addressTitle) if addressTitle=='NULL' else ("'"+str(addressTitle)+"'")
		with connection.cursor() as cursor:
			cursor.execute("call post_library.sp_addAddress('"+str(uuid_post)+"', '"+str(countryTitle)+"', '"+str(cityTitle)+"', " + addressTitle + ", "+str(latitude)+", "+str(longitude)+");")
			connection.commit()
	
	pass

def AddImg(uuid_post='', _img_url=''):
	"""Добавление изображения в БД (post_library)"""
	print ("uuid post:{0} img url:{1}".format(uuid_post,_img_url))
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call post_library.sp_addImg('"+str(uuid_post)+"', '"+str(_img_url)+"');")
			connection.commit()






























# addreses = list()
# def Addreses():
# 	global addreses
# 	addreses = list()
# 	if connection != None: # Если подключение создано
# 		with connection.cursor() as cursor:
# 			cursor.execute("""
# 				SELECT 
# 					`address`.`id`,
# 					`address`.`uuid`,
# 					`address`.`uuid_city`,
# 					`address`.`title`,
# 					`address`.`latitude`,
# 					`address`.`longitude`
# 				FROM `post_library`.`address`;
# 				""")
# 			for i in cursor.fetchall():
# 				# print(i)
# 				addreses.append(
# 					Address(
# 						id=i['id'], 
# 						uuid=i['uuid'], 
# 						uuid_city=i['uuid_city'], 
# 						title=i['title'], 
# 						latitude=i['latitude'], 
# 						longitude=i['longitude']))
# 	return addreses
# class Address(object):
# 	def __init__(self, id=None, uuid=None, uuid_city=None, title=None, latitude=None, longitude=None):
# 		self.id = id
# 		self.uuid = uuid
# 		self.uuid_city = uuid_city
# 		self.title = title
# 		self.latitude = latitude
# 		self.longitude = longitude
# 	pass
# 	def get_city(self):
# 		if connection != None: # Если подключение создано
# 			with connection.cursor() as cursor:
# 				cursor.execute("""
# 					SELECT 
# 						`city`.`id`,
#     					`city`.`uuid`,
#     					`city`.`uuid_country`,
#     					`city`.`title`
# 					FROM `post_library`.`city`
# 					WHERE `city`.`uuid` LIKE {0};
# 					""".format(self.uuid_city))
				
# 				return cursor.fetchall()
# 		return None
# 	def set_city(self, value):
# 		if connection != None: # Если подключение создано
# 			with connection.cursor() as cursor:
# 				cursor.execute("""
# 					SELECT 
# 						`city`.`id`,
#     					`city`.`uuid`,
#     					`city`.`uuid_country`,
#     					`city`.`title`
# 					FROM `post_library`.`city`;
# 					""")
# 	city = property(get_city, set_city)
# if __name__=="__main__":
# 	Connect(
# 		host='172.16.17.67', 
# 		user='usr_post_lib', 
# 		password='MnM32RtQt', 
# 		db='post_library')
# 	# print(Addreses)
# 	Addreses()
# 	for i in addreses:
# 		print(i.city)

	CloseConnect()

# if __name__=="__main__":
# 	Connect(
# 		host=post_library_host(), 
# 		user=post_library_user(), 
# 		password=post_library_password(), 
# 		db=post_library_db())

		
# 	CloseConnect()