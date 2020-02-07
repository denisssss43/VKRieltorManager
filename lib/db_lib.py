"""Либа для взаимодействия с базой данных"""
import uuid
from datetime import datetime, timedelta
import pymysql
from contextlib import closing
from pymysql.cursors import DictCursor
import ast 
import copy

connection = None # Объект подключения к бд
# NOTE:Изменено и откомментировано полностью
def Connect(host='', user='', password='', db=''):
	"""Подключение к БД"""
	global connection
	connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8', cursorclass=DictCursor)
# NOTE:Изменено и откомментировано полностью
def CloseConnect():
	"""Закрытие подключения к БД"""
	global connection
	if connection != None: 
		connection.close()
		connection = None

def GetCountry(uuid=''):
	"""Получение страны по uuid"""
	result = None
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM test.country WHERE uuid='"+str(uuid)+"';")
			result = cursor.fetchone()
	return result

def GetCity(uuid=''):
	"""Получение города по uuid"""
	result = None
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM test.city WHERE uuid='"+str(uuid)+"';")
			result = cursor.fetchone()
	return result

def GetCommunity():
	"""Получение списка групп, по которым необходимо собирать информацию"""
	result = None
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM test.community;")
			result = cursor.fetchall()
	return result

def AddCommunity(countryTitle='', cityTitle='', communityURL=''):
	"""Добавление сообщества в БД"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call test.sp_addCommunity('"+str(countryTitle)+"', '"+str(cityTitle)+"', '"+str(communityURL)+"');")
			connection.commit()
	pass

def AddPost(communityURL='', description='', dateTime=datetime.now(), price=0.0, url='', telephones=[]):
	"""Добавление поста в БД"""
	result = None
	
	if price <= 0: return result

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call test.sp_addPost('"+str(communityURL)+"','"+str(description)[:1024]+"','"+str(dateTime)+"',"+str(price)+",'"+str(url)+"');")
			result = cursor.fetchone()
			for num in telephones:
				AddTelephone(result['uuid'], str(num))
			connection.commit()

	return result

def AddTelephone(uuid_post='',telephone=''):
	"""Добавление телефона в БД"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call test.sp_addTelephone('"+str(uuid_post)+"', '"+str(telephone)+"');")
			connection.commit()
	pass

def AddAddress(uuid_post='', countryTitle='', cityTitle='', addressTitle='', latitude=0.0, longitude=0.0):
	"""Добавление адреса в БД"""

	if connection != None: # Если подключение создано
		addressTitle = str(addressTitle) if addressTitle=='NULL' else ("'"+str(addressTitle)+"'")
		with connection.cursor() as cursor:
			cursor.execute("call test.sp_addAddress('"+str(uuid_post)+"', '"+str(countryTitle)+"', '"+str(cityTitle)+"', " + addressTitle + ", "+str(latitude)+", "+str(longitude)+");")
			connection.commit()
	
	pass

def AddImg(uuid_post='', _img_url=''):
	"""Добавление изображения в БД"""
	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call test.sp_addImg('"+str(uuid_post)+"', '"+str(_img_url)+"');")
			connection.commit()