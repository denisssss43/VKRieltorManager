

# from flask import Flask, request, render_template

# app = Flask(__name__)

# from app import routes

@app.route('/')
def index():
	return '...'


@app.route('/search')
def home():

	result = 'Параметры поиска:'

	for i in request.args:
		result += '<br/>{0}:{1}'.format(i,request.args.getlist(i))

	return result

@app.route('/stat/<country>/<city>')
def stat(country = None, city = None):

	result = 'Страна {0} Город {1}'.format(country, city)

	return render_template(
		'stat.html',
		title='Stat', 
		country=country,
		city=city)