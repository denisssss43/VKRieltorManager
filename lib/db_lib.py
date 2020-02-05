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
def Connect(host='localhost', user='root', password='MnM32RtQt', db='test'):
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

def GetGroups():
	"""Получение списка групп, по которым необходимо собирать информацию"""
	result = list()
	
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public9751268', 'url_group':'public9751268'})
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public123114913', 'url_group':'public9751268'})
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public105543780', 'url_group':'public9751268'})
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public76867861', 'url_group':'public9751268'})
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public80318218', 'url_group':'public9751268'})
	
	pass


def AddPost(communityURL='', description='', dateTime=datetime.now(), price=0.0, url=''):
	"""Добавление поста в БД"""

	if connection != None: # Если подключение создано
		with connection.cursor() as cursor:
			cursor.execute("call test.sp_addPost('"+str(communityURL)+"','"+str(description)[:1024]+"','"+str(dateTime)+"',"+str(price)+",'"+str(url)+"');")
			connection.commit()
	pass

def AddAddress(uuid_post='', countryTitle='', cityTitle='', addressTitle='', latitude=0.0, longitude=0.0):
	"""Добавление адреса в БД"""
	# call test.sp_addAddress('qwe', 'qwe', 'qwe', 'qwe', qwe, qwe);

	if connection != None: # Если подключение создано
		addressTitle = str(addressTitle) if addressTitle=='NULL' else ("'"+str(addressTitle)+"'")
		print(addressTitle)
		with connection.cursor() as cursor:
			cursor.execute("call test.sp_addAddress('"+str(uuid_post)+"', '"+str(countryTitle)+"', '"+str(cityTitle)+"', " + addressTitle + ", "+str(latitude)+", "+str(longitude)+");")
			connection.commit()
	
def AddTelephone():
	"""Добавление телефона в БД"""
	# call test.sp_addTelephone('qwe', 'we');
	pass