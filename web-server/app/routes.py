from app import app, request, render_template
from parser.lib.db_post import CloseConnect, Connect
from parser.lib.cfg.cfg import *

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
	Connect(
		host=post_library_host(), 
		user=post_library_user(), 
		password=post_library_password(), 
		db=post_library_db())
	CloseConnect()

	return render_template(
		'stat.html',
		title='Stat', 
		country=country,
		city=city)