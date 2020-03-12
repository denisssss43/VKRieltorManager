"""Либа взаимодействия с конфигурационным файлом"""

import sqlite3
import os

connection = None # Объект подключения
cursor = None # Объект курсора
path = ""

def Connect():
	"""Подключение к конфигурационному файлу"""
	global connection, cursor

	# connection = sqlite3.connect(sys.path[0].replace('\\', '/')+'/cfg.db')

	# print ('full path -', os.path.abspath(path+'cfg.db'))
	connection = sqlite3.connect(os.path.abspath(path+'cfg.db'))
	cursor = connection.cursor()
	
	sql = """ 
		CREATE TABLE IF NOT EXISTS "param" (
		"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		"name" TEXT NOT NULL UNIQUE,
		"value" TEXT NOT NULL,
		"description" TEXT NOT NULL);"""

	cursor.execute(sql)

	connection.commit()

def Close():
	"""Закрытие подключения к конфигурационному файлу"""
	global connection, cursor

	connection.commit()
	connection.close()

	connection = None
	cursor = None
	pass

def GetParam(name):
	"""Получение значения параметра по имени name=value"""
	global connection, cursor
	result = None
	Connect()
	result = cursor.execute('SELECT value FROM param WHERE name=? LIMIT 1;', [(name)]).fetchone()[0] # fetchall() or fetchone()
	Close()
	return result

def SetParam(**kwargs):
	"""Передача значения в идин или несколько параметров (создание параметра в случае если он не создан) SetParamm(name=('text','описание'), name=(1), ...)"""
	global connection, cursor

	Connect()
	
	for key, value in kwargs.items():
		if type(value) == tuple:
			if len(value) > 1:
				cursor.execute("REPLACE INTO param(name, value, description) VALUES('{0}','{1}','{2}');".format(str(key), str(value[0]), str(value[1])))
			elif len(value) == 1:
				cursor.execute("REPLACE INTO param(name, value, description) VALUES('{0}','{1}','{2}');".format(str(key), str(value[0]), ''))
			else:
				cursor.execute("REPLACE INTO param(name, value, description) VALUES('{0}','{1}','{2}');".format(str(key), str(value), ''))
		else:
			cursor.execute("REPLACE INTO param(name, value, description) VALUES('{0}','{1}','{2}');".format(str(key), str(value), ''))

	Close()


def __set_param():
	SetParam(
		post_library_host=('172.16.17.67','значение хост библиотеки постов'), 
		post_library_user=('usr_post_lib', 'имя пользователя с которого будет осуществлятся взаимодействие с библиотекой постов'), 
		post_library_password=('MnM32RtQt', 'пароль пользователя с которого будет осуществляться взаимодействие с библиотекой постов'), 
		post_library_db=('post_library', 'наименование библиотеки постов'),
		
		# user_library_host=('localhost', ''), 
		# user_library_user=('root', ''), 
		# user_library_password=('...', ''), 
		# user_library_db=('user_library', ''),
		
		call_add_post_delay_ms=(60000, 'значение задержки запроса на добавление поста, мс'))

if __name__ == "__main__":

	path = "vk_parser/lib/cfg/"
	__set_param()

	path = "web-server/"
	__set_param()
	
	Connect()
	result = cursor.execute("SELECT * FROM param;").fetchall()
	Close()

	f = open('vk_parser/lib/cfg/cfg.py','w', encoding='utf-8')
	f.write('"""Либа представлений параметров конфигурационного файла"""\n\n\n')
	f.write('from . import GetParam\n\n\n')
	
	for param in result:
		f.write(
			'def {0}():\n    """представление параметра {0}{1}"""\n    return GetParam("{0}")\n\n'.format(
				param[1],
				" - "+param[3] if param[3] != "" else ""))

	f.close()
	
