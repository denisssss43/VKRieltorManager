"""Либа представлений параметров конфигурационного файла"""


from . import GetParam


def post_library_host():
    """представление параметра post_library_host - значение хост библиотеки постов"""
    return GetParam("post_library_host")

def post_library_user():
    """представление параметра post_library_user - имя пользователя с которого будет осуществлятся взаимодействие с библиотекой постов"""
    return GetParam("post_library_user")

def post_library_password():
    """представление параметра post_library_password - пароль пользователя с которого будет осуществляться взаимодействие с библиотекой постов"""
    return GetParam("post_library_password")

def post_library_db():
    """представление параметра post_library_db - наименование библиотеки постов"""
    return GetParam("post_library_db")

def call_add_post_delay_ms():
    """представление параметра call_add_post_delay_ms - значение задержки запроса на добавление поста, мс"""
    return GetParam("call_add_post_delay_ms")

