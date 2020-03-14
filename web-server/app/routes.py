from app import app, request
from flask import render_template
import sys

sys.path.append('..')

from vk_parser.lib.cfg.cfg import *
from vk_parser.lib.db_post import *

nav = [
	{'title':'About', 'href':'/'}, 
	{'title':'Map', 'href':'/map'}, 
	{'title':'Search', 'href':'/search'},
	{'title':'1', 'href':'#'},
	{'title':'2', 'href':'#'},
	{'title':'3', 'href':'#'}]

@app.route('/')
@app.route('/index')
def index():
	# ans = render_template('map.html', nav=nav, title='Map')

	# while ans.find('  ') > -1: ans = ans.replace('  ',' ')
	# while ans.find('\n\n') > -1: ans = ans.replace('\n\n','\n')
	# while ans.find('\t\t') > -1: ans = ans.replace('\t\t','\t')

	# print(ans)
	return render_template(
		'index.html',
		title='About',  
		nav=nav)


@app.route('/map')
@app.route('/map/<country>/<city>')
def map(country=None, city=None):
	# Connect(
	# 	host=post_library_host(), 
	# 	user=post_library_user(), 
	# 	password=post_library_password(), 
	# 	db=post_library_db())
	# communities = GetCommunity()
	# # for i in communities: print (i)
	# CloseConnect()

	print ('country={0} city={1}'.format(country, city))

	countries = [
		{ 
			'isSelected': False, 
			'title': 'Россия',
			'cities': [
				{
					'isSelected': False, 
					'title': 'Красноярск',
					'addresses': [
						{'latitude': 55.995242, 'longitude': 92.897402, 'title':'Газеты Красноярский Рабочий проспект, 164'},
						{'latitude': 55.993965, 'longitude': 92.908823, 'title':'Академика Вавилова, 2а/5'},
						{'latitude': 55.989014, 'longitude': 92.904613, 'title':'Семафорная, 257'},]},
				{
					'isSelected': False, 
					'title': 'Железногорск',
					'addresses': [
						{'latitude': 56.251553, 'longitude': 93.529015, 'title':'22 Партсъезда, 14'},
						{'latitude': 56.234246, 'longitude': 93.549251, 'title':'Курчатова проспект, 42'},
						{'latitude': 56.224922, 'longitude': 93.5124, 'title':'Ленинградский проспект, 67'},]},]},
		{ 
			'isSelected': False, 
			'title': 'Россия',
			'cities': [
				{
					'isSelected': False, 
					'title': 'Красноярск',
					'addresses': [
						{'latitude': 55.995242, 'longitude': 92.897402, 'title':'Газеты Красноярский Рабочий проспект, 164'},
						{'latitude': 55.993965, 'longitude': 92.908823, 'title':'Академика Вавилова, 2а/5'},
						{'latitude': 55.989014, 'longitude': 92.904613, 'title':'Семафорная, 257'},
					]},
				{
					'isSelected': False, 
					'title': 'Железногорск',
					'addresses': [
						{'latitude': 56.251553, 'longitude': 93.529015, 'title':'22 Партсъезда, 14'},
						{'latitude': 56.234246, 'longitude': 93.549251, 'title':'Курчатова проспект, 42'},
						{'latitude': 56.224922, 'longitude': 93.5124, 'title':'Ленинградский проспект, 67'},]},]},]

	return render_template('map.html', nav=nav, title='Map')


@app.route('/stat/<country>/<city>')
def stat(country = None, city = None):
	return render_template(
		'stat.html',
		title='Stat', 
		country=country,
		city=city)


@app.route('/search')
# @app.route('/search/<country>/<city>')
def search():
	return render_template(
		'search.html',
		title='Search',  
		nav=nav)



# @app.route('/search')
# def home():
# 	result = 'Параметры поиска:'
# 	for i in request.args:
# 		result += '<br/>{0}:{1}'.format(i,request.args.getlist(i))
# 	return result
