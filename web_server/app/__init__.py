import os
import sys

# sys.path.append('.')
print ('web_server.app run abs_PATH {0}'.format(os.path.abspath('')))

from flask import Flask, request, render_template

app = Flask(
    __name__,
    static_folder = 'static')
app.debug=True

from web_server.app import routs
