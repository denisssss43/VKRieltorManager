"""Либа взаимодействия с конфигурационным файлом"""

import sqlite3

connection = None # Объект подключения
cursor = None # Объект курсора

def Connect():
    """Подключение к конфигурационному файлу"""
    global connection, cursor

    connection = sqlite3.connect("res/cfg.db")
    cursor = connection.cursor()
    
    sql = """ 
        CREATE TABLE IF NOT EXISTS "paramm" (
	    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	    "name"	TEXT NOT NULL UNIQUE,
	    "value"	TEXT NOT NULL);"""

    cursor.execute(sql)

    connection.commit()
def Close():
    """Закрытие подключения к конфигурационному файлу"""
    global connection, cursor

    connection.commit()
    connection.close()

    connection = None
    cursor = None
    pass

def GetParamm(name=''):
    """Получение значения параметра по имени"""
    global connection, cursor
    result = None
    Connect()
    result = cursor.execute(
        """SELECT value FROM paramm WHERE name=? LIMIT 1;""",
        [(name)]).fetchone()[0] # fetchall() or fetchone()
    Close()
    return result

def SetParamm(name='', value=''):
    """Передача значения в параметр (создание параметра в случае если он не создан)"""
    global connection, cursor
    Connect()

    sql = """REPLACE INTO paramm(name, value) VALUES(?,?);"""
    
    cursor.execute(sql,(name, value))
            

    Close()

if __name__ == "__main__":
    SetParamm(name='host', value='localhost')
    SetParamm(name='user', value='root')
    SetParamm(name='password', value='MnM32RtQt')
    SetParamm(name='db', value='test')