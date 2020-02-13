"""Либа представлений параметров конфигурационного файла"""


from cfg_lib import GetParam


def post_library_host():
    """представление параметра post_library_host - значение хост библиотеки постов"""
    return GetParamm("post_library_host")

def post_library_user():
    """представление параметра post_library_user"""
    return GetParamm("post_library_user")

def post_library_password():
    """представление параметра post_library_password"""
    return GetParamm("post_library_password")

def post_library_db():
    """представление параметра post_library_db"""
    return GetParamm("post_library_db")

def user_library_host():
    """представление параметра user_library_host"""
    return GetParamm("user_library_host")

def user_library_user():
    """представление параметра user_library_user"""
    return GetParamm("user_library_user")

def user_library_password():
    """представление параметра user_library_password"""
    return GetParamm("user_library_password")

def user_library_db():
    """представление параметра user_library_db"""
    return GetParamm("user_library_db")

def call_add_post_delay_ms():
    """представление параметра call_add_post_delay_ms"""
    return GetParamm("call_add_post_delay_ms")

