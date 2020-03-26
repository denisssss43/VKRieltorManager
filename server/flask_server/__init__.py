from flask import Flask

web_app = Flask(__name__, static_folder = 'static')

from server.flask_server import web_api, web_server