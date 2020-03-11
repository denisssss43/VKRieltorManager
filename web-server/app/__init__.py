from flask import Flask, request, render_template

app = Flask(__name__)

import routes


app.static_folder = 'static'