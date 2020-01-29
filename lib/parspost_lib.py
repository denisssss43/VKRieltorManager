"""Либа для поиска и парса поста"""

import requests
from bs4 import BeautifulSoup
import re 
import uuid
from datetime import datetime, timedelta
import pymysql
from contextlib import closing
from pymysql.cursors import DictCursor
import ast 
import copy 

# Изменено и откомментировано полностью
def AddressYandex(string, country='Россия', city='Красноярск'):
	'''Нормализация адресса строки и определение его параметров'''

	# Параметр текста в яндекс картах
	text = (country + ' ' + city + string).replace(' ','%20')
	
	response = requests.get(	# Получение ответа по запрошенному тексту
		'https://yandex.ru/maps/62/moscow/?text='+ text + '&z=17')

	# Определение параметров ответа
	for meta in BeautifulSoup(response.text, 'html.parser').find_all('meta'):
		# Проверка связи параметров с параметрами адреса
		if meta.get('property') == 'og:title' and str(meta.get('content')).lower().find((country+', '+city+', ').lower()) == 0:
			latitude = 0.0	# широта (перпендикулярна экватору)
			longitude = 0.0	# Долгота (по экватору)
			
			# Определение долготы и широты
			for ch in BeautifulSoup(response.text, 'html.parser').find_all('script', class_='config-view'):

				patern = re.compile(	# Объявление патерна регулярного выражения
					r'("coordinates":\[\d+.\d+,\d+.\d+\])')

				# Поиск совпадений 
				result = patern.findall(ch.text)[0].replace('"coordinates":[','').replace(']','').split(',')
				
				latitude = result[1]	# Определение широты 
				longitude = result[0]	# Определение долготы
			
			response.close() # Закрытие ответа по запросу 
			return {	# Возврат результата
				'address':		meta.get('content'),
				'latitude': 	latitude,	# широта (перпендикулярна экватору)
				'longitude': 	longitude}	# Долгота (по экватору)
			
	response.close()
	return {
		'address':		'none',
		'latitude': 	0.0,	# широта (перпендикулярна экватору)
		'longitude': 	0.0}	# Долгота (по экватору) 




if __name__ == "__main__":
	while(True):
		try:
			print (datetime.datetime.now(), 'Connect')
			db.Connect()

			for i in range(3):
				db.SearchFromGroupWithoutAddress(g_id='123114913', g_title='', offset=i*10, country='Россия', city='Красноярск')
				db.SearchFromGroupWithoutAddress(g_id='105543780', g_title='', offset=i*10, country='Россия', city='Красноярск')
				db.SearchFromGroupWithoutAddress(g_id='', g_title='arendav24', offset=i*10, country='Россия', city='Красноярск')
				db.SearchFromGroupWithoutAddress(g_id='', g_title='arenda.v.krasnoyarske', offset=i*10, country='Россия', city='Красноярск')
				db.SearchFromGroupWithoutAddress(g_id='76867861', g_title='', offset=i*10, country='Россия', city='Красноярск') 
				db.SearchFromGroupWithoutAddress(g_id='80318218', g_title='', offset=i*10, country='Россия', city='Красноярск')

			db.CloseConnect()
			print ('	CloseConnect')
		except: pass
    
    pass