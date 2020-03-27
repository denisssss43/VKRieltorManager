from server.flask_server import web_app
from flask import request, render_template

@web_app.route('/')
@web_app.route('/index')
def index():
    return 'index'