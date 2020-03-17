"""Либа представлений параметров конфигурационного файла"""


from . import GetParam

class Config(object):
	""" Объект-конфигуратор """

	# Представление параметра post_library_host - значение хост библиотеки постов
	post_library_host = GetParam("post_library_host")

	# Представление параметра post_library_user - имя пользователя с которого будет осуществлятся взаимодействие с библиотекой постов
	post_library_user = GetParam("post_library_user")

	# Представление параметра post_library_password - пароль пользователя с которого будет осуществляться взаимодействие с библиотекой постов
	post_library_password = GetParam("post_library_password")

	# Представление параметра post_library_db - наименование библиотеки постов
	post_library_db = GetParam("post_library_db")

	# Представление параметра call_add_post_delay_ms - значение задержки запроса на добавление поста, мс
	call_add_post_delay_ms = GetParam("call_add_post_delay_ms")

	pass