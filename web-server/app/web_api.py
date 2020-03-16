from app import app, request
from flask import render_template
import sys

sys.path.append('..')

from vk_parser.lib.cfg.cfg import *
from vk_parser.lib.db_post import *

# @app.route('/api/')


@app.route('/api')
@app.route('/api/')
def api(): return 'Молодец, да это web-api'


@app.route('/api/')
def api_GetVinegret(): return 'Молодец, да это web-api'