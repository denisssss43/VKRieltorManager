"""Либа для поиска и парса поста"""

import requests
from bs4 import BeautifulSoup
import re 
from datetime import datetime, timedelta
import datetime

# NOTE:Изменено и откомментировано полностью
def AddressYandex(string, country='', city=''):
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
				'address': str(meta.get('content')).upper().replace(
					str(country + ', ' + city + ', ').upper(), ''),
				'latitude': latitude,	# широта (перпендикулярна экватору)
				'longitude': longitude}	# Долгота (по экватору)
			
	response.close() # Закрытие ответа по запросу 
	return { # Возврат пустого результата
		'address': 'NULL',
		'latitude': 0.0,	# широта (перпендикулярна экватору)
		'longitude': 0.0}	# Долгота (по экватору) 
# NOTE:Изменено и откомментировано полностью
def AddressFromDescription(description, country='', city=''):
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
	pi_text_list = BeautifulSoup(wall_item, 'html.parser').find_all(class_='pi_text')

	if len(pi_text_list) < 1: return ' '

	pi_text = str(pi_text_list[0])

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
	charSet = '1234567890 йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm#_-+()/\\,.!;:?'

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
def DescriptionClean(description):
	"""Итоговая отчистка и нормализация описания"""

	if len(description) < 1: return description

	# Отчистка описания от номеров телефонов
	paternTelephones = re.compile( # Объявление патерна регулярного выражения
		r'(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?')
	# Поиск исходной строки номера в описании
	match = paternTelephones.search(description)
	while match:
		# Удаление исходной строки из описания
		description = description.replace(str(match[0]),'<номер удален>')
		# Поиск следующей исходной строки номера в описании
		match = paternTelephones.search(description)

	# Отчистка описания от хэштэгов
	paternHashtags = re.compile( # Объявление патерна регулярного выражения
		r'#\S+')
	# Поиск исходной строки в описании	
	match = paternHashtags.search(description)
	while match:
		# Удаление исходной строки из описания
		description = description.replace(str(match[0]),'')
		# Поиск следующей исходной строки в описании
		match = paternHashtags.search(description) 

	# Нормализация знаков припинания
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
	paternLinks = re.compile( # Объявление патерна регулярного выражения
		r'(https: /)?([a-zA-Z0-9_-]{2,}. )+[a-zA-Z]{1,}(/[a-zA-Z0-9_-]+)*') 
	# Поиск исходной строки в описании	     
	match = paternLinks.search(description)
	while match:
		# Удаление исходной строки из описания
		description = description.replace(str(match[0]),'<ссылка удалена>')
		# Поиск следующей исходной строки в описании
		match = paternLinks.search(description)

	#   
	paternDate = re.compile( # Объявление патерна регулярного выражения
		r'(0[1-9]|[1-3][1-9]). (0[1-9]|1[1-9])(. ([0-9]{4}|[0-9]{2}))?') 
	# Поиск исходной строки в описании	 
	match = paternDate.search(description)
	while match:
		# Удаление исходной строки из описания
		description = description.replace(str(match[0]),str(match[0]).replace(' ',''))
		# Поиск следующей исходной строки в описании
		match = paternDate.search(description)

	if len(description) < 1: return description
	if description[0] == ' ': description = description.replace(' ', '', 1)

	return description
# NOTE:Изменено и откомментировано полностью
def ImgPars(wall_item):
	"""Получение изображений из поста во вконтакте"""
	# thumb_map_img thumb_map_img_as_div
	result = list()

	for div_img in BeautifulSoup(wall_item, 'html.parser').find_all('div', class_='thumb_map_img thumb_map_img_as_div'):
		result.append(div_img.get('data-src_big').split('|')[0])

	return result
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
# NOTE:Изменено и откомментировано полностью
def HashtagPars(description):
	"""Получение хэштэгов из описания поста"""
	
	paternHashtags = re.compile( # Объявление патерна регулярного выражения
		r'#\S+')

	# Инициализация списка хэштэгов
	hashtags = list()

	# Нохождение первой исходной строки хэштэга в описании
	match = paternHashtags.search(description)
	while match:
		# Запись исходной строки найденого хэштэга в описании
		hashtags.append(str(match[0])) 

		# Удаление исходной строки из описания
		description = description.replace(hashtags[len(hashtags)-1],'')

		# Список символов которые необходимо оставить
		charSet = '1234567890йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm#_-'

		# отчистка хэштэга от посторонних символов
		for char in hashtags[len(hashtags)-1]:
			if (charSet.find(char.lower()) == -1): 
				hashtags[len(hashtags)-1] = hashtags[len(hashtags)-1].replace(char,'')

		# Поиск следующей исходной строки в описании
		match = paternHashtags.search(description)   
	#
	return hashtags
# NOTE:Изменено и откомментировано полностью
def DatePars(wall_item):
	"""Получение даты публикации поста"""

	# Список всех сокращений в дате вк
	m = "дек ноя окт сен авг июл июн мая апр мар фев янв вчера сегодня".split(' ')[::-1]
	# Исходная строка с датой
	str_date = ''
	# Определенное значение минут
	minute=0
	# Определенное значение часов
	hour=12
	# Определенное значение дня
	day = -1
	# Определенное значение месяца
	month = -1
	# Определенное значение года
	year = -1

	# Получение и обработка даты поста
	for wi_date in BeautifulSoup(wall_item, 'html.parser').find_all('a', class_='wi_date'):
		
		# Получение не обработанной даты
		str_date = str(wi_date.get_text())

		# print(str_date)

		# Получение времени
		patern = re.compile( # Объявление патерна регулярного выражения
			r'(\w+:\w+)')
		# Нохождение исходной строки
		match = patern.search(str_date)
		while match:
			# Запись исходной строки
			minute = int(match[0].split(':')[1])
			hour = int(match[0].split(':')[0])
			break
	
		# Получение года
		patern = re.compile( # Объявление патерна регулярного выражения
			r'(\w{4})')
		# Нохождение исходной строки
		match = patern.search(str_date)
		while match:
			# Запись исходной строки
			year = str(match[0])
			break

		# Получение дня
		patern = re.compile( # Объявление патерна регулярного выражения
			r'(^\w+)')
		# Нохождение исходной строки
		match = patern.search(str_date)
		while match:
			# Запись исходной строки
			day = str(match[0])
			break

		# Получение месяца
		patern = re.compile( # Объявление патерна регулярного выражения
			r'([a-zA-Zа-яА-Я]{3,})')
		# Нохождение исходной строки
		match = patern.search(str_date)
		while match:
			# Запись исходной строки
			month = [x for x in range(len(m)) if m[x] == match[0]][0]

			# print('1 month', month)
			
			if month == 0: # В случае если дата указана как сегодня
				day = datetime.datetime.now().day
				month = datetime.datetime.now().month
				year = datetime.datetime.now().year
			if month == 1: # В случае если дата указана как вчера
				# Получение вчерашней даты
				date = datetime.datetime.now() - datetime.timedelta(days=1)
				day = date.day
				month = date.month
				year = date.year
			else: month = month - 1
			
			if year == -1: # В случае если год не был указан в исходной дате
				if month <= datetime.datetime.now().month:
					year = datetime.datetime.now().year 
				else: 
					year = datetime.datetime.now().year-1

			# print('2 month', month)
			break

		year = int(year)
		month = int(month)
		day = int(day)
		hour = int(hour)
		minute = int(minute)

		# print('year',year, 'month',month, 'day',day, 'hour',hour, 'minute',minute)
		# print(datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute))

	return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
# NOTE:Изменено и откомментировано полностью
def LinkPars(wall_item):
	"""Получение ссылки на пост"""

	for post_anchor in BeautifulSoup(wall_item, 'html.parser').find_all('a', class_='post__anchor anchor'):
		return str('https://vk.com/'+str(post_anchor.get('name')).replace('post','wall'))
	return None
# NOTE:Изменено и откомментировано полностью
def PricePars(description):
	"""Получение стоимости предложения из описания"""

	# Список найденых цен в описании
	price = list()

	# Нормализация цен в описании
	patern = re.compile( # Объявление патерна регулярного выражения
		r'((\d|\s)(тыс|т)[., ]{1,3})')
	match = patern.findall(description)
	for i in match:
		_old = str(i[0])
		_new = _old.replace('тыс','000').replace('т','000')
		description = description.replace(_old, _new)

	# Поиск цен в описании
	patern = re.compile( # Объявление патерна регулярного выражения
		r'((\W|\D)[0-9]{1,3}[., ]{0,3}[0-9]{3}(\W|\D))')
	# Запись исходной строки найденого номера в описании
	match = patern.findall(description)
	for i in match:
		# Запись исходной найденной в описании
		string = str(i[0])
		# отчистка исходной строки от посторонних символов
		for char in string:
			if ('1234567890'.find(char.lower()) == -1): 
				string = string.replace(char, '')
		price.append(float(string))

	if len(price) < 1: return 0.0
	
	# Возврат максимальной цены
	return max(price)
# NOTE:Изменено и откомментировано полностью
def WallItemPars(wall_item=''):
	"""Парсинг поста сообщества"""

	# Описание нормализовано и записано
	description = DescriptionPars(wall_item) 
	# Получение телефонных номеров
	telephones = TelephonePars(description)
	# Получение хэштэгов
	hashtags = HashtagPars(description)
	# Отчистка описания 
	description = DescriptionClean(description)
	# Цена предложения	
	price = PricePars(description)

	if price <= 0: # Если цена определилась как нулевая
		return {
			'date': DatePars(wall_item), 				# Получение даты публикации
			'link_community': '',		# Ссылка на сообщество
			'link': LinkPars(wall_item),					# Получение ссылки на запись во вкантакте
			'description': '',			# Описание 
			'price': 0.0,				# Цена предложения
			'address': {				# Адрес
				'address': 'NULL', 
				'latitude': 0.0, 
				'longitude': 0.0}, 
			'telephones': list(),		# Получение телефонных номеров
			'img_urls': list(),			# Получение ссылок на изображение
			'hashtags': list()}			# Получение телефонных номеров

	return {
		'date': DatePars(wall_item), 		# Получение даты публикации
		'link_community': '',				# Ссылка на сообщество
		'link': LinkPars(wall_item),		# Получение ссылки на запись во вкантакте
		'description': description,			# Описание 
		'price': PricePars(description),	# Цена предложения
		'address': {						# Адрес
			'address': 'NULL', 
			'latitude': 0.0, 
			'longitude': 0.0}, 
		'telephones': telephones,			# Получение телефонных номеров
		'img_urls': ImgPars(wall_item),		# Получение ссылок на изображение
		'hashtags': hashtags}				# Получение телефонных номеров

# NOTE:Изменено и откомментировано полностью
def WallItemSearch(country='', city='', id_group='', url_group='', offset=0):
	"""Поиск сырых постов в указанной группе
	(Без адреса)"""

	# Список обработаных постов
	_list = list()

	# Указанная группа
	group = {'country':country, 'city':city, 'id_group':id_group, 'url_group':url_group}
	
	# получение идентификатора группы
	if url_group == '':
		g_ = 'https://m.vk.com/' + group['id_group']
	else:
		g_ = group['url_group']
	
	# Запрос в группу для получения постов
	response = requests.get(g_ + '?offset=' + str(offset)) # + '&own=1')
	# Подготовка ответа для дальнейшего парса
	vk_com = BeautifulSoup(response.text, 'html.parser') 
	# Закрытие ответа
	response.close() 
	
	# Загрузка списка постов
	for wall_item in vk_com.find_all(class_='wall_item'): 
		# try: 
		# Парс загруженного поста
		wall_item = WallItemPars(str(wall_item))
		# Проверка определения цены 
		# В сучае, когда цена не определена дальнейшая обработка прекращается
		wall_item['link_community'] = g_
		# Добавление обработанного поста в список
		_list.append(wall_item)
		# except: pass

	return _list

if __name__ == "__main__":

	pass