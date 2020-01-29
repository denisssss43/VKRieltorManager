"""Либа для поиска и парса поста"""

import requests
from bs4 import BeautifulSoup
import re 
import uuid
from datetime import datetime, timedelta
from contextlib import closing
import ast 
import copy 

# NOTE:Изменено и откомментировано полностью
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
# NOTE:Изменено и откомментировано полностью
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

# NOTE:Изменено и откомментировано полностью
def DescriptionPars(wall_item):
	"""Получение описания из записи поста"""

	# Обработка описания
	pi_text = str(BeautifulSoup(wall_item, 'html.parser').find_all(class_='pi_text')[0])

	# Отчистка от раскрытия полного текста
	for pi_text_more in BeautifulSoup(wall_item,'html.parser').find_all(class_='pi_text_more'): 
		pi_text = pi_text.replace(str(pi_text_more),'') 
	
	# отчистка от тегов ссылок
	for link in BeautifulSoup(str(pi_text), 'html.parser').find_all('a'): 
		pi_text = pi_text.replace(str(link), link.get_text()) 
	
	# отчистка от эмодзи
	for emoji in BeautifulSoup(str(pi_text), 'html.parser').find_all('img', class_='emoji'): 
		pi_text = pi_text.replace(str(emoji), '') 
	
	# отчистка от html тегов
	for zoom_text in BeautifulSoup(str(pi_text), 'html.parser').find_all(class_='pi_text zoom_text'): 
		pi_text = pi_text.replace(str(zoom_text), zoom_text.get_text()) 
	
	# Отчистка от html тегов
	pi_text = pi_text.replace(
		'<br/>',' ').replace(
			'</div>','').replace(
				'<div class="pi_text">','').replace(
					'<span style="display:none">','').replace(
						'<span>','').replace(
							'</span>','')
	
	# Список символов которые необходимо оставить
	charSet = '1234567890 йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm#_-+()/\\,.!;:?\n'

	# отчистка описания от посторонних символов
	for char in pi_text:
		if (charSet.find(char.lower()) == -1): 
			pi_text = pi_text.replace(char,' ')
	
	# отчистка от двойных пробелов
	while pi_text.find('  ') > -1: 
		pi_text = pi_text.replace('  ',' ')
	
	# нормализация знаков припинания
	return pi_text.replace(
		' .','. ').replace(
			' ,',', ').replace(
				' !','! ').replace(
					' ?','? ').replace(
						' :',': ').replace(
							' ;','; ').replace(
								'( ','( ').replace(
									' )',') ')
# NOTE:Изменено и откомментировано полностью
def TelephonePars(description):
	"""Получение телефонных номеров из описания поста"""
	
	paternTelephones = re.compile( # Объявление патерна регулярного выражения
		r'(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?')
	
	# Инициализация списка телефонных номеров
	telephones = list()

	# Нохождение первой исходной строки номера в описании
	match = paternTelephones.search(description)
	
	while match:
		# Запись исходной строки найденого номера в описании
		telephones.append(str(match[0])) 
		# Удаление исходной строки из описания
		description = description.replace(telephones[len(telephones)-1],'')
		# Нормализация найденного номера и приведения к виду
		for char in telephones[len(telephones)-1]:
			if ('1234567890'.find(char.lower()) == -1): 
					telephones[len(telephones)-1] = telephones[len(telephones)-1].replace(char,'')
		telephones[len(telephones)-1] = '+7'+telephones[len(telephones)-1][-10:]
		# Поиск следующей исходной строки номера в описании
		match = paternTelephones.search(description)
	#
	return telephones

def WallItemPars(wall_item=''):
	"""Парсинг поста сообщества"""
	# Описание нормализовано и записано
	description = DescriptionPars(wall_item) 
	# Получение телефонных номеров
	telephones = TelephonePars(description)
	# Получение телефонных номеров
	hashtags = HashtagPars(description)
	# Отчистка
	description = CleanDescription(description)
	return {'date': None, # ParsDate(wall_item), # Получение даты
			'link': ParsLink(wall_item),		# Получение ссылки на запись во вкантакте
			'description': description,			# Описание 
			'price': ParsPrice(description),	# Цена предложения
			'telephones': telephones,			# Получение телефонных номеров
			'hashtags': hashtags}				# Получение телефонных номеров

def WallItemSearch():
	"""Поиск сырых постов в указанных группах
	(Без адреса)"""

	groupList = list()
	groupList.append({'country':'Россия', 'city':'Красноярск', 'id_group':'public105543780'})
	groupList.append({'country':'Россия', 'city':'Красноярск', 'id_group':'arendav24'})


	for group in groupList:
		g_ = group['id_group']
		offset = 0

		response = requests.get('https://m.vk.com/' + g_ + '?offset=' + str(offset) + '&own=1')

		vk_com = BeautifulSoup(response.text, 'html.parser') 

		response.close() 
		
		# Список постов
		_list = list()

		# Загрузка списка постов
		for wall_item in vk_com.find_all(class_='wall_item'): 
			try: _list.append(WallItemParserWithoutAddress(str(wall_item)))
			except: pass

		try:
			with connection.cursor() as cursor:
				# print ('saved ')
				for row in _list:
					# print ('saved ', row['link'], row['price'])
					cursor.execute(AddPostWithoutAddress(
						link=row['link'], 
						community='https://m.vk.com/' + g_, 
						city=city, 
						description=row['description'], 
						price=row['price']))
					for telephone in row['telephones']:
						cursor.execute(AddTelephone(
							link=row['link'], 
							telephone=telephone))
					for hashtag in row['hashtags']:
						cursor.execute(AddHashtag(
							link=row['link'], 
							hashtag=hashtag))
			connection.commit()
		except: pass
	

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
