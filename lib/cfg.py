"""Либа представлений параметров конфигурационного файла"""


from cfg_lib import GetParam


def post_library_host():
    """представление параметра post_library_host - значение хост библиотеки постов"""
    return GetParam("post_library_host")

def post_library_user():
    """представление параметра post_library_user"""
    return GetParam("post_library_user")

def post_library_password():
    """представление параметра post_library_password"""
    return GetParam("post_library_password")

def post_library_db():
    """представление параметра post_library_db"""
    return GetParam("post_library_db")

def user_library_host():
    """представление параметра user_library_host"""
    return GetParam("user_library_host")

def user_library_user():
    """представление параметра user_library_user"""
    return GetParam("user_library_user")

def user_library_password():
    """представление параметра user_library_password"""
    return GetParam("user_library_password")

def user_library_db():
    """представление параметра user_library_db"""
    return GetParam("user_library_db")

def call_add_post_delay_ms():
    """представление параметра call_add_post_delay_ms"""
    return GetParam("call_add_post_delay_ms")

