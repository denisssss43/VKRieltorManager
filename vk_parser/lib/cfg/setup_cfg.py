"""  """
import sys
sys.path.append('.')

from vk_parser.lib.cfg import SetParam, GetParam, Connect, Close, path

def __setup():
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
	__setup()

	path = "web-server/"
	__setup()
	
	connection = Connect()
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
				'\t# Представление параметра {0}{1}\n\t{0} = GetParam("{0}")\n\n'.format(
					param[1], 
					" - "+param[3] if param[3] != "" else ""))
		
		f.write('\tpass')
		f.close()
	