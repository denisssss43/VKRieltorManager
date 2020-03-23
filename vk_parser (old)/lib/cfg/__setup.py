def __setup(path=''):
	import sys
	sys.path.append('..')

	from vk_parser.lib.cfg import SetParam
	
	SetParam(
		path,
		post_library_host=('172.16.17.67','значение хост библиотеки постов'), 
		post_library_user=('usr_post_lib', 'имя пользователя с которого будет осуществлятся взаимодействие с библиотекой постов'), 
		post_library_password=('MnM32RtQt', 'пароль пользователя с которого будет осуществляться взаимодействие с библиотекой постов'), 
		post_library_db=('post_library', 'наименование библиотеки постов'),
		
		# user_library_host=('localhost', ''), 
		# user_library_user=('root', ''), 
		# user_library_password=('...', ''), 
		# user_library_db=('user_library', ''),
		
		call_add_post_delay_ms=(60000, 'значение задержки запроса на добавление поста, мс'))