""" Генератор конфигурационного модуля """

if __name__ == "__main__":
	# sys.path.append('.')

	import os
	from server._lib.cfg import SetParam, GetParam, Connect, Close
	from server._lib.cfg.__setup import __setup

	path = os.path.abspath('server/_lib/cfg/')
	
	__setup(path)
	"""
	# Вызов функции внесения в конфигурационный файл необходимых значений 
	# (вместо __setup(path)
	SetParam(
		path,
		post_library_host=('...','Значение хост библиотеки постов'), 
		post_library_user=('...', 'Имя пользователя с которого будет осуществлятся взаимодействие с библиотекой постов'), 
		post_library_password=('...', 'Пароль пользователя с которого будет осуществляться взаимодействие с библиотекой постов'), 
		post_library_db=('...', 'Наименование библиотеки постов'),)
	"""
	
	connection = Connect(path)
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
			'server/_lib/cfg/cfg.py','w',
			encoding='utf-8')
		f.write('"""Либа представлений параметров конфигурационного файла"""\n\n\n')
		f.write('from server._lib.cfg import GetParam\n\n')
		f.write('class Config(object):\n')
		f.write('\t""" Объект-конфигуратор """\n\n')
		for param in result:
			f.write(
				'\t# Представление параметра {0}{1}\n\t{0} = GetParam("{2}", "{0}")\n\n'.format(
					param[1], 
					" - "+param[3] if param[3] != "" else "",
					path.replace('\\', '\\\\')))
		
		f.write('\tpass')
		f.close()
	