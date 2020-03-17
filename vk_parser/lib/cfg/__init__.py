"""Либа взаимодействия с конфигурационным файлом"""

import sqlite3
import os

path = "vk_parser/lib/cfg/"

def Connect():
	"""Подключение к конфигурационному файлу"""
	connection = None

	try: connection = sqlite3.connect(os.path.abspath(path+'cfg.db'))
	except: connection = sqlite3.connect(os.path.abspath('cfg.db'))
	
	if connection != None:
		connection.cursor().execute(
			""" 
			CREATE TABLE IF NOT EXISTS "param" (
			"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
			"name" TEXT NOT NULL UNIQUE,
			"value" TEXT NOT NULL,
			"description" TEXT NOT NULL);
			""")
		connection.commit()
	
	return connection

def Close(connection):
	"""Закрытие подключения к конфигурационному файлу"""
	if connection != None:
		connection.commit()
		connection.close()
	pass

def GetParam(name):
	"""Получение значения параметра по имени name=value"""
	connection = Connect()
	result = None
	
	if connection != None:
		result = connection.cursor().execute(
			'SELECT value FROM param WHERE name=? LIMIT 1;', 
			[(name)]).fetchone()[0]
		Close(connection)

	return result

def SetParam(**kwargs):
	"""Передача значения в идин или несколько параметров (создание параметра в случае если он не создан) SetParamm(name=('text','описание'), name=(1), ...)"""
	connection = Connect()	
	if connection != None:
		for key, value in kwargs.items():
			if type(value) == tuple:
				if len(value) > 1:
					connection.cursor().execute(
						"REPLACE INTO param(name, value, description) VALUES('{0}','{1}','{2}');".format(
							str(key), 
							str(value[0]), 
							str(value[1])))
				elif len(value) == 1:
					connection.cursor().execute(
						"REPLACE INTO param(name, value, description) VALUES('{0}','{1}','{2}');".format(
							str(key), 
							str(value[0]), 
							''))
				else:
					connection.cursor().execute(
						"REPLACE INTO param(name, value, description) VALUES('{0}','{1}','{2}');".format(
							str(key), 
							str(value), 
							''))
			else:
				connection.cursor().execute(
					"REPLACE INTO param(name, value, description) VALUES('{0}','{1}','{2}');".format(
						str(key), 
						str(value), 
						''))

		Close(connection)
