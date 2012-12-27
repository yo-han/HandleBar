""" HandleBar webserver """

import os 
from lib import *

projectDir = os.path.abspath(os.path.dirname(__file__))

app = Bottle()
filesTable = Files()

@app.route('/')
@view('index')
def index(appName="HandleBar"):
	bottle.TEMPLATES.clear()
	
	
	return dict(appName=appName)

@app.route('/media/<filepath:path>')
def static(filepath):
    return static_file(filepath, root=projectDir + '/media/')

run(app, host='localhost', port=8082)