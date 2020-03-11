from flask import Flask, request, render_template

app = Flask(__name__, static_folder = 'static')
app.debug=True

from app import routes
