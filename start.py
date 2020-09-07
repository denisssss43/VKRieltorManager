"""
Запуск проекта
"""

from server.pars_server import ParserAsync
import os

cmd = """echo start...

cd {2}

# echo Подготовка к запуску сервера flask:
# echo FLASK_ENV=development
# echo # set FLASK_ENV=development

# echo FLASK_APP={1}/flask_server:web_app
# set FLASK_APP={1}/flask_server:web_app
# flask run

echo makemigrations
{0}\\python.exe {1}\\django_server\\manage.py makemigrations

echo migrate
{0}\\python.exe {1}\\django_server\\manage.py migrate

echo runserver
{0}\\python.exe {1}\\django_server\\manage.py runserver

""".format(
		os.path.abspath('Scripts'), 
		os.path.abspath('server'), 
		os.path.abspath('')
	).replace('\\','/'
	).replace('\n\n', '& echo --- & '
	).replace('\n', ' & ')

if __name__ == "__main__":
	# ParserAsync().start()
	os.system(cmd)