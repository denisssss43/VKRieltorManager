"""
Запуск проекта
"""

import os
cmd = """echo start...
cd {2}

echo Подготовка к запуску сервера flask:
echo FLASK_ENV=development
echo # set FLASK_ENV=development

echo FLASK_APP={1}:web_app
set FLASK_APP={1}:web_app

flask run

""".format(
		os.path.abspath('Scripts'), 
		os.path.abspath('server'), 
		os.path.abspath('')
	).replace('\\','/').replace('\n\n', '& echo --- & ').replace('\n', ' & ')


if __name__ == "__main__":
	os.system(cmd)