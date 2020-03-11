from flask import Flask, request, render_template

app = Flask(__name__)
app.debug=True
# app.static_folder = 'static'

from app import routes
