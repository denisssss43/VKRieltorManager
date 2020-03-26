"""
Установка и настройка виртуального окружения проекта
"""

import os
cmd = """echo setup ...

echo Установка виртуальной среды: 
echo install venv VKRieltorManager
cd .. & py -m venv VKRieltorManager

echo Запуск виртуальной среды ({0}/activate): 
{0}/activate

echo Обновление pip и установка/обновление всех необходимых библиотек:
echo upgrade pip
python -m pip install --upgrade pip

echo install Flask
echo # pip install Flask

echo Вывод установленных библиотек виртуальной среды:
echo # pip list

echo Остановка виртуальной машины
deactive

echo Строки с пометкой '#' были пропущены.

""".format(
		os.path.abspath('Scripts/'), 
		os.path.abspath('web_server/'), 
		os.path.abspath('')
	).replace('\\','/').replace('\n\n', '& echo --- & ').replace('\n', ' & ')


if __name__ == "__main__":
	print ('\nsetup_start run abs_PATH {0} \n\n'.format(os.path.abspath('')))
	os.system(cmd)