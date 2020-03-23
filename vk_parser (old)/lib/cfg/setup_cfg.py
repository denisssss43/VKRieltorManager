""" Генератор конфигурационного модуля """

if __name__ == "__main__":
	import sys
	sys.path.append('.')

	from vk_parser.lib.cfg import SetParam, GetParam, Connect, Close
	from vk_parser.lib.cfg.__setup import __setup
	
	# Адрес по которому будет создан конфигурационный файл
	__setup("vk_parser/lib/cfg/")
	"""
	# Вызов функции внесения в конфигурационный файл необходимых значений
	SetParam(
		"vk_parser/lib/cfg/",
		post_library_host=('...','Значение хост библиотеки постов'), 
		post_library_user=('...', 'Имя пользователя с которого будет осуществлятся взаимодействие с библиотекой постов'), 
		post_library_password=('...', 'Пароль пользователя с которого будет осуществляться взаимодействие с библиотекой постов'), 
		post_library_db=('...', 'Наименование библиотеки постов'),)
	"""
	
	# Адрес по которому будет создан конфигурационный файл
	__setup("web-server/")
	"""
	# Вызов функции внесения в конфигурационный файл необходимых значений
	SetParam(
		post_library_host=('...','Значение хост библиотеки постов'), 
		post_library_user=('...', 'Имя пользователя с которого будет осуществлятся взаимодействие с библиотекой постов'), 
		post_library_password=('...', 'Пароль пользователя с которого будет осуществляться взаимодействие с библиотекой постов'), 
		post_library_db=('...', 'Наименование библиотеки постов'),)
	"""
	
	connection = Connect("vk_parser/lib/cfg/")
	result = None
	
	if connection != None:
		result = connection.cursor().execute(
			"""
			SELECT * 
			FROM param;
			""").fetchall()
		Close(connection)

	if result != None:	
		f = open(
			'vk_parser/lib/cfg/cfg.py','w',
			encoding='utf-8')
		f.write('"""Либа представлений параметров конфигурационного файла"""\n\n\n')
		f.write('from . import GetParam\n\n')
		f.write('class Config(object):\n')
		f.write('\t""" Объект-конфигуратор """\n\n')
		for param in result:
			f.write(
				'\t# Представление параметра {0}{1}\n\t{0} = GetParam("vk_parser/lib/cfg/", "{0}")\n\n'.format(
					param[1], 
					" - "+param[3] if param[3] != "" else ""))
		
		f.write('\tpass')
		f.close()
	