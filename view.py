""" HandleBar webserver """

import os, socket 
from lib import *
from app import *

projectDir = os.path.abspath(os.path.dirname(__file__))

app = Bottle()
filesTable = Files()

@app.route('/')
@view('index')
def index(appName="HandleBar"):
	bottle.TEMPLATES.clear()
	
	fileList = filesTable.list()
	
	return dict(appName=appName, list=fileList)

@app.route('/media/<filepath:path>')
def static(filepath):
    return static_file(filepath, root=projectDir + '/media/')

host = socket.gethostbyname(socket.gethostname())

run(app, host=host, port=8082)