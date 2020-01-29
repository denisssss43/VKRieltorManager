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

connection = None

def Connect(host='localhost', user='root', password='MnM32RtQt', db='dbo'):
	global connection
	connection = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8', cursorclass=DictCursor)
def CloseConnect():
	global connection
	if connection != None: 
		connection.close()

def AddPost(link, community, address, city, description, price):
	return "CALL `dbo`.`add_post`('"+link+"', '"+community+"', '"+address+"', '"+city+"', '"+description+"', "+str(price)+");"
def AddPostWithoutAddress(link, community, city, description, price):
	return "CALL `dbo`.`add_post`('"+link+"', '"+community+"', NULL, '"+city+"', '"+description+"', "+str(price)+");"
def AddTelephone(link, telephone):
	return "CALL `dbo`.`add_telephone`('"+link+"', '"+telephone+"');"
def AddHashtag(link, hashtag):
	return "CALL `dbo`.`add_hashtag`('"+link+"', '"+hashtag+"');"
def AddAddress(uuid_post, address, city):
	return "call dbo.add_post_address('"+uuid_post+"', '"+address+"', '"+city+"');"

def AddressYandex(address, country='Россия', city='Красноярск'):
	response = requests.get('https://yandex.ru/maps/62/moscow/?text='+ (country + ' ' + city + address).replace(' ','%20') + '&z=17')
	for meta in BeautifulSoup(response.text, 'html.parser').find_all('meta'):
		if meta.get('property') == 'og:title' and str(meta.get('content')).lower().find((country+', '+city+', ').lower()) == 0:
			response.close()
			return meta.get('content')
	response.close()
	return 'none'

def AddressPosition(address):
	latitude = 0.0
	longitude = 0.0

	print('https://yandex.ru/maps/62/moscow/?text='+ (address).replace(' ','%20') + '&z=17')
	response = requests.get('https://yandex.ru/maps/62/moscow/?text='+ (address).replace(' ','%20') + '&z=17')

	i = ''
	for ch in BeautifulSoup(response.text, 'html.parser').find_all('script', class_='config-view'):
		patern = re.compile(r'("coordinates":\[\d+.\d+,\d+.\d+\])')
		result = patern.findall(ch.text)[0].replace('"coordinates":[','').replace(']','').split(',')
		latitude = result[1]
		longitude = result[0]

	response.close()

	return {
		'latitude': latitude,	# широта (перпендикулярна экватору)
		'longitude': longitude	# Долгота (по экватору)
	}

def AddressFromDescription(description, country='Россия', city='Красноярск'):
	for char in description:
		if ('1234567890 йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm'.find(char.lower()) == -1): 
			description = description.replace(char,' ')
	description = description.replace('номер удален', ' ').replace('ссылка удалена', ' ')

	# проверка на дубликаты
	for char in ' ':
		while description.lower().find(char+char) != -1:
			description = description.replace(char+char, char)
	for count in range(3)[::-1]:
		patern = re.compile(r'((\w+ ){'+str(count+1)+r'}([домаДОМА]{1,4}( )?)?[0-9]{1,3}( )?\w?( ))')
		for address in patern.findall(description): return AddressYandex(address[0], country='Россия', city='Красноярск')
	return 'none'

def ParsDate(wall_item):
	return datetime.now()
	for wi_date in BeautifulSoup(wall_item, 'html.parser').find_all('a', class_='wi_date'):
		str_date = str(wi_date.get_text())
	if str_date.find('вчера') > -1: str_date =str((datetime.now() - timedelta(days=1)).date())
	elif str_date.find('сегодня') > -1: str_date =str((datetime.now() - timedelta(days=1)).date())
	return datetime.now() # str_date
def ParsHashtags(description):
	# Получение хэштэгов
	paternHashtags = re.compile(r'#\S+')
	match = paternHashtags.search(description)
	hashtags = list()
	while match:
		# Запись исходной строки найденого хэштэга в описании
		hashtags.append(str(match[0])) 
		# Удаление исходной строки из описания
		description = description.replace(hashtags[len(hashtags)-1],'')
		# отчистка хэштэга от посторонних символов
		for char in hashtags[len(hashtags)-1]:
			if ('1234567890йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm#_-'.find(char.lower()) == -1): 
				hashtags[len(hashtags)-1] = hashtags[len(hashtags)-1].replace(char,'')
		# Поиск следующей исходной строки в описании
		match = paternHashtags.search(description)   
	#
	return hashtags
def ParsTelephones(description):
	# Получение телефонных номеров
	paternTelephones = re.compile(r'(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?')
	match = paternTelephones.search(description)
	telephones = list()
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
def ParsPrice(description):
	price = 0.0
	paternPrice = re.compile(r'(\W|\D)[0-9]{1,3}[., ]{0,3}[0-9]{3}(\W|\D)')
	match = paternPrice.search(description)
	while match:
		# Запись исходной строки найденого номера в описании
		string = str(match[0])
		# отчистка описания от посторонних символов
		for char in string:
			if ('1234567890'.find(char.lower()) == -1): 
				string = string.replace(char, '')
		price = float(string)
		break
	if price != 0.0: return price
	match = re.search(r'(\d|\s)(тыс|т)[., ]{1,3}', description)
	while match:
		# Запись исходной строки найденого номера в описании
		_old = str(match[0])
		_new = _old.replace('тыс','000').replace('т','000')
		description = description.replace(_old, _new)
		break
	match = paternPrice.search(description)
	while match:
		# Запись исходной строки найденого номера в описании
		string = str(match[0])
		# отчистка описания от посторонних символов
		for char in string:
			if ('1234567890'.find(char.lower()) == -1): 
				string = string.replace(char, '')
		price = float(string)
		break
	#
	return price
def ParsLink(wall_item):
	for post_anchor in BeautifulSoup(wall_item, 'html.parser').find_all('a', class_='post__anchor anchor'):
		return str('https://vk.com/'+str(post_anchor.get('name')).replace('post','wall'))
	return None
def ParsDescription(wall_item):
	# Обработка описания
	pi_text = str(BeautifulSoup(wall_item, 'html.parser').find_all(class_='pi_text')[0])
	# Отчистка от раскрытия полного текста
	for pi_text_more in BeautifulSoup(wall_item,'html.parser').find_all(class_='pi_text_more'): pi_text = pi_text.replace(str(pi_text_more),'') 
	# отчистка от тегов ссылок
	for link in BeautifulSoup(str(pi_text), 'html.parser').find_all('a'): pi_text = pi_text.replace(str(link), link.get_text()) 
	# отчистка от эмодзи
	for emoji in BeautifulSoup(str(pi_text), 'html.parser').find_all('img', class_='emoji'): pi_text = pi_text.replace(str(emoji), '') 
	# отчистка от html тегов
	for zoom_text in BeautifulSoup(str(pi_text), 'html.parser').find_all(class_='pi_text zoom_text'): pi_text = pi_text.replace(str(zoom_text), zoom_text.get_text()) 
	# Отчистка от html тегов
	pi_text = pi_text.replace('<br/>',' ').replace('</div>','').replace('<div class="pi_text">','').replace('<span style="display:none">','').replace('<span>','').replace('</span>','')
	# отчистка описания от посторонних символов
	for char in pi_text:
		if ('1234567890 йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm#_-+()/\\,.!;:?\n'.find(char.lower()) == -1): pi_text = pi_text.replace(char,' ')
	# отчистка от двойных пробелов
	while pi_text.find('  ') > -1: pi_text = pi_text.replace('  ',' ')
	# нормализация знаков припинания
	return pi_text.replace(' .','. ').replace(' ,',', ').replace(' !','! ').replace(' ?','? ').replace(' :',': ').replace(' ;','; ').replace('( ','( ').replace(' )',') ')
def CleanDescription(description):
	# Отчистка описания от номеров телефонов и хэштэгов
	paternTelephones = re.compile(r'(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?')
	match = paternTelephones.search(description)
	while match:
		# Удаление исходной строки из описания
		description = description.replace(str(match[0]),'<номер удален>')
		# Поиск следующей исходной строки номера в описании
		match = paternTelephones.search(description)
	#
	paternHashtags = re.compile(r'#\S+')
	match = paternHashtags.search(description)
	while match:
		# Удаление исходной строки из описания
		description = description.replace(str(match[0]),'')
		# Поиск следующей исходной строки в описании
		match = paternHashtags.search(description) 

	# нормализация знаков припинания
	for char in '.,!?:;':
		description = description.replace(char, char+' ')
		while description.lower().find(' '+char) != -1 or description.lower().find(' '+char+' ') != -1:
			while description.lower().find('  ') != -1:
				description = description.replace('  ', ' ')
			description = description.replace(' '+char, char+' ')
			description = description.replace(' '+char+' ', char+' ')

	# проверка на дубликаты
	for char in ' #_-+()/\\,.!?\n':
		while description.lower().find(char+char) != -1:
			description = description.replace(char+char, char)
			
	# Отчистка описания от номеров ссылок  
	paternLinks = re.compile(r'(https: /)?([a-zA-Z0-9_-]{2,}. )+[a-zA-Z]{1,}(/[a-zA-Z0-9_-]+)*')      
	match = paternLinks.search(description)
	while match:
		# Удаление исходной строки из описания
		description = description.replace(str(match[0]),'<ссылка удалена>')
		# Поиск следующей исходной строки в описании
		match = paternLinks.search(description)

	#   
	paternDate = re.compile(r'(0[1-9]|[1-3][1-9]). (0[1-9]|1[1-9])(. ([0-9]{4}|[0-9]{2}))?')  
	match = paternDate.search(description)
	while match:
		# Удаление исходной строки из описания
		description = description.replace(str(match[0]),str(match[0]).replace(' ',''))
		# Поиск следующей исходной строки в описании
		match = paternDate.search(description)
	
	if description[0] == ' ': description = description.replace(' ', '', 1)

	return description

def TimeToPoint(addressFrom='', addressTo=''):
	# Запрос на получение времени маршрута
	response = requests.get('https://www.google.com/search?q=маршрут+пешком+от+'+str(addressFrom).replace(' ','+')+'+до+'+str(addressTo).replace(' ','+')+'&ie=UTF-8')
	# разбор ответа
	bs = BeautifulSoup(response.text, 'html.parser')
	response.close()
	vk_c = bs.find_all(class_='FCUp0c rQMQod AWuZUe')
	vk_c = BeautifulSoup(str(vk_c[0]), 'html.parser') if len(vk_c) > 0 else BeautifulSoup(str('-1'), 'html.parser')
	string =  vk_c.get_text().replace('.','').replace(' ','')
	# Конвертация в чистые минуты
	hours = 0
	minutes = 0
	match = re.search(r'[1234567890]{1,}ч', string)
	while match: hours = int(match[0].replace('ч', ''))*60; break;
	match = re.search(r'[1234567890]{1,}мин', string)
	while match: minutes = int(match[0].replace('мин', ''))+hours; break;
	return minutes

def WallItemParser(wall_item=''):
	# Описание нормализовано и записано
	description = ParsDescription(wall_item) 
	# Получение телефонных номеров
	telephones = ParsTelephones(description)
	# Получение телефонных номеров
	hashtags = ParsHashtags(description)
	# Отчистка
	description = CleanDescription(description)
	return {'date': ParsDate(wall_item), # Получение даты
			'link': ParsLink(wall_item), # Получение ссылки на запись во вкантакте
			'address': AddressFromDescription(description),
			'description': description,
			'price': ParsPrice(description),
			'telephones': telephones, # Получение телефонных номеров
			'hashtags': hashtags} # Получение телефонных номеров
def WallItemParserWithoutAddress(wall_item=''):
	# Описание нормализовано и записано
	description = ParsDescription(wall_item) 
	# Получение телефонных номеров
	telephones = ParsTelephones(description)
	# Получение телефонных номеров
	hashtags = ParsHashtags(description)
	# Отчистка
	description = CleanDescription(description)
	return {# 'date': ParsDate(wall_item), # Получение даты
			'link': ParsLink(wall_item), # Получение ссылки на запись во вкантакте
			'description': description,
			'price': ParsPrice(description),
			'telephones': telephones, # Получение телефонных номеров
			'hashtags': hashtags} # Получение телефонных номеров

def SearchFromGroup(g_id='', g_title='', offset=0, country='Россия', city='Красноярск'): 
	global connection
	g_ = ''
	if (g_id == '' and g_title == ''): return 0
	if (g_id != ''): g_ = 'public' + g_id
	else: g_ = g_title
	response = requests.get('https://m.vk.com/' + g_ + '?offset=' + str(offset) + '&own=1')
	vk_com = BeautifulSoup(response.text, 'html.parser')    
	response.close() 
	_list = list()
	for wall_item in vk_com.find_all(class_='wall_item'): 
		try: _list.append(WallItemParser(str(wall_item)))
		except: pass
	try:
		with connection.cursor() as cursor:
			for row in _list:
				cursor.execute(AddPost(
					link=row['link'], 
					community='https://m.vk.com/' + g_, 
					address=str(row['address']), 
					city=city, 
					description=row['description'], 
					price=0))
				for telephone in row['telephones']:
					cursor.execute(AddTelephone(
						link=row['link'], 
						telephone=telephone))
				for hashtag in row['hashtags']:
					cursor.execute(AddHashtag(
						link=row['link'], 
						hashtag=hashtag))
				print (row['link'], row['address'])
		connection.commit()
	except: pass
def SearchFromGroupWithoutAddress(g_id='', g_title='', offset=0, country='Россия', city='Красноярск'):
	global connection
	if (g_id == '' and g_title == ''): return 0
	g_ = ('public' + g_id) if g_id != '' else g_title
	response = requests.get('https://m.vk.com/' + g_ + '?offset=' + str(offset) + '&own=1')
	vk_com = BeautifulSoup(response.text, 'html.parser')    
	response.close() 
	_list = list()
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
	Connect()
	with connection.cursor() as cursor:
		while (True):
			cursor.execute("SELECT * FROM dbo.address WHERE latitude is null and longitude is null LIMIT 1;")
			adress = copy.deepcopy(cursor.fetchone())
			if (adress != None):
				position = AddressPosition(adress['title'])

				cursor.execute("call dbo.add_address_position('"+adress['uuid']+"', "+position['latitude']+", "+position['longitude']+");")
				connection.commit()

				print(adress, position)

	CloseConnect()