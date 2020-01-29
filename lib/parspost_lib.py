"""Либа для поиска и парса поста"""

import requests
from bs4 import BeautifulSoup
import re 
import uuid
from datetime import datetime, timedelta
from contextlib import closing
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

				patern = re.compile( # Объявление патерна регулярного выражения
					r'("coordinates":\[\d+.\d+,\d+.\d+\])')

				# Поиск совпадений 
				result = patern.findall(ch.text)[0].replace('"coordinates":[','').replace(']','').split(',')
				
				latitude = result[1]	# Определение широты 
				longitude = result[0]	# Определение долготы
			
			response.close() # Закрытие ответа по запросу 
			return { # Возврат результата
				'address':		str(meta.get('content')).upper().replace(str(country + ', ' + city + ', ').upper(), ''),
				'latitude': 	latitude,	# широта (перпендикулярна экватору)
				'longitude': 	longitude}	# Долгота (по экватору)
			
	response.close() # Закрытие ответа по запросу 
	return { # Возврат пустого результата
		'address':		'NULL',
		'latitude': 	0.0,	# широта (перпендикулярна экватору)
		'longitude': 	0.0}	# Долгота (по экватору) 
# Изменено и откомментировано полностью
def AddressFromDescription(description, country='Россия', city='Красноярск'):
	"""Поиск адреса в описании"""

	# Удаление лишних символов
	for char in description:
		if ('1234567890 йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm'.find(char.lower()) == -1): 
			description = description.replace(char,' ')
	
	# Очистка заглушек удаленных номеров и ссылок
	description = description.replace('номер удален', ' ').replace('ссылка удалена', ' ')

	# Удаление двойных пробелов
	for char in ' ':
		while description.lower().find(char+char) != -1:
			description = description.replace(char+char, char)
	
	# Результат
	result = {'address':'NULL', 'latitude':0.0, 'longitude':0.0} 

	# Определение адреса
	for count in range(3)[::-1]:
		patern = re.compile( # Объявление патерна регулярного выражения
			r'((\w+ ){'+str(count+1)+r'}([домаДОМА]{1,4}( )?)?[0-9]{1,3}( )?\w?( ))')

		# Прогон результатов поиска регуляркой 
		for address in patern.findall(description):
			# Определение является ли результат адресом 
			result = AddressYandex(address[0], country='Россия', city='Красноярск')
			# Выход из прогона при нахождении адреса
			if result['address'] != 'NULL': break

		# Выход из определения адреса при нахождении адреса
		if result['address'] != 'NULL': break
	
	return result



if __name__ == "__main__":
	# print(
	# 	AddressYandex(
	# 		"Крас раб 102", 
	# 		country='Россия', 
	# 		city='Красноярск'))

	print(
		AddressFromDescription(
			"Сдаётся: КОМНАТА в 4-комн. квартире (Собственник, без комиссии) Район: Центральный Адрес: г. Красноярск, ул. Белинского, д. 3 Стоимость: 9200 (Свет и вода включены в стоимость) Контакты: 89029265016 https://vk.com/evgeniyaderyavko Доп.: Комната большая, закрывается на ключ. Есть всё для комфортного проживания: 2х сп кровать, шкаф угловой, стол, стиральная машинка. Кухня вся укомплектована, WI-FI, ванна и туалет в отличном состоянии, раздельные. В квартире хороший ремонт и хорошая мебель. Рядом остановка в любою точку города, мед институт в 10 минутах, автовокзал, ТЦ на Стрелке, ТЦ Комсомолл, продуктовые магазины, парк.", 
			country='Россия', 
			city='Красноярск'))

#	while(True):
#		try:
#			print (datetime.datetime.now(), 'Connect')
#			db.Connect()
#
#			for i in range(3):
#				db.SearchFromGroupWithoutAddress(g_id='123114913', g_title='', offset=i*10, country='Россия', city='Красноярск')
#				db.SearchFromGroupWithoutAddress(g_id='105543780', g_title='', offset=i*10, country='Россия', city='Красноярск')
#				db.SearchFromGroupWithoutAddress(g_id='', g_title='arendav24', offset=i*10, country='Россия', city='Красноярск')
#				db.SearchFromGroupWithoutAddress(g_id='', g_title='arenda.v.krasnoyarske', offset=i*10, country='Россия', city='Красноярск')
#				db.SearchFromGroupWithoutAddress(g_id='76867861', g_title='', offset=i*10, country='Россия', city='Красноярск') 
#				db.SearchFromGroupWithoutAddress(g_id='80318218', g_title='', offset=i*10, country='Россия', city='Красноярск')
#
#			db.CloseConnect()
#			print ('	CloseConnect')
#		except: pass