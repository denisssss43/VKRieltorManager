"""
Установка и настройка виртуального окружения проекта
"""

import os
from server._lib.post_parser import ParserAsync
cmd = """echo setup ...

echo Установка виртуальной среды: 
echo install venv VKRieltorManager
cd .. & py -m venv VKRieltorManager

cd {2}

echo Запуск виртуальной среды ({0}/activate): 
{0}/activate.bat

echo Обновление pip и установка/обновление всех необходимых библиотек:
echo upgrade pip
python -m pip install --upgrade pip
echo install Flask
pip install Flask
echo install db-sqlite3
pip install db-sqlite3
echo install PyMySQL
pip install PyMySQL
echo install requests
pip install requests
echo install beautifulsoup4
pip install beautifulsoup4

echo Создание конфиг-файла:
py server\\_lib\\cfg\\setup_cfg.py

echo Вывод установленных библиотек виртуальной среды:
pip list

""".format(
		os.path.abspath('Scripts'), 
		os.path.abspath('server'), 
		os.path.abspath('')
	).replace('\\','/').replace('\n\n', '& echo --- & ').replace('\n', ' & ')


if __name__ == "__main__":
	ParserAsync().start()
	os.system(cmd)