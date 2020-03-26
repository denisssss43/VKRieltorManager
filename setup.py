"""
Установка и настройка виртуального окружения проекта
"""

import os
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

echo Создание конфиг-файла:
py server\\_lib\cfg\\setup_cfg.py

echo Вывод установленных библиотек виртуальной среды:
pip list

""".format(
		os.path.abspath('Scripts'), 
		os.path.abspath('web_server'), 
		os.path.abspath('')
	).replace('\\','/').replace('\n\n', '& echo --- & ').replace('\n', ' & ')


if __name__ == "__main__":
	os.system(cmd)