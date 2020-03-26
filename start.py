"""
Запуск проекта
"""

import os
cmd = """start...

echo Подготовка к запуску сервера flask:
echo FLASK_ENV=development
set FLASK_ENV=development

echo FLASK_APP={1}/__init__.py
set FLASK_APP={1}/__init__.py
flask run

""".format(
		os.path.abspath('Scripts/'), 
		os.path.abspath('web_server/'), 
		os.path.abspath('')
	).replace('\\','/').replace('\n\n', '& echo --- & ').replace('\n', ' & ')


if __name__ == "__main__":
	print ('\nsetup_start run abs_PATH {0} \n\n'.format(os.path.abspath('')))
	os.system(cmd)