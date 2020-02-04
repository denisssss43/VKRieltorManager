"""Либа для взаимодействия с базой данных"""
import requests
import uuid
from datetime import datetime, timedelta
import pymysql
from contextlib import closing
from pymysql.cursors import DictCursor
import ast 
import copy 

connection = None

def Connect(host='localhost', user='root', password='MnM32RtQt', db='dbo'):
	global connection
	connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8', cursorclass=DictCursor)
def CloseConnect():
	global connection
	if connection != None: 
		connection.close()



def GetGroups():
	"""Получение списка групп, по которым необходимо собирать информацию"""
	result = list()
	
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public9751268', 'url_group':'public9751268'})
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public123114913'})
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public105543780'})
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public76867861'})
	result.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public80318218'})
	
	pass


def AddPost(communityTitle='',):


	# call test.sp_addPost(
	# 	'йцу', # 
	# 	'цу', 
	# 	'цу', 
	# 	йцу, 
	# 	'йцу');
	pass

def AddAddress():
	# call test.sp_addAddress('qwe', 'qwe', 'qwe', 'qwe', qwe, qwe);
	
	pass

def AddTelephone():
	# call test.sp_addTelephone('qwe', 'we');
	pass