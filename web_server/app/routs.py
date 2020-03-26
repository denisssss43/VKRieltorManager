from web_server.app import app, request


# index or main routs
@app.route('/')
@app.route('/index')
def index():
    return 'index'