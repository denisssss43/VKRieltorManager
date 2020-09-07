"""Либа представлений параметров конфигурационного файла"""


from server._lib.cfg import GetParam

class Config(object):
	""" Объект-конфигуратор """

	# Представление параметра post_library_host - значение хост библиотеки постов
	post_library_host = GetParam("C:\\Users\\Denis\\Documents\\GitHub\\VKRieltorManager\\server\\_lib\\cfg", "post_library_host")

	# Представление параметра post_library_user - имя пользователя с которого будет осуществлятся взаимодействие с библиотекой постов
	post_library_user = GetParam("C:\\Users\\Denis\\Documents\\GitHub\\VKRieltorManager\\server\\_lib\\cfg", "post_library_user")

	# Представление параметра post_library_password - пароль пользователя с которого будет осуществляться взаимодействие с библиотекой постов
	post_library_password = GetParam("C:\\Users\\Denis\\Documents\\GitHub\\VKRieltorManager\\server\\_lib\\cfg", "post_library_password")

	# Представление параметра post_library_db - наименование библиотеки постов
	post_library_db = GetParam("C:\\Users\\Denis\\Documents\\GitHub\\VKRieltorManager\\server\\_lib\\cfg", "post_library_db")

	# Представление параметра call_add_post_delay_ms - значение задержки запроса на добавление поста, мс
	call_add_post_delay_ms = GetParam("C:\\Users\\Denis\\Documents\\GitHub\\VKRieltorManager\\server\\_lib\\cfg", "call_add_post_delay_ms")

	# Представление параметра offset_add_post - кол-во экранов от последнего, которое будет просматриваться в добавленных группах
	offset_add_post = GetParam("C:\\Users\\Denis\\Documents\\GitHub\\VKRieltorManager\\server\\_lib\\cfg", "offset_add_post")

	pass