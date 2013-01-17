""" HandleBar webserver """

import os, socket 
from lib import *
from app import *

projectDir = os.path.abspath(os.path.dirname(__file__))

bottle.TEMPLATE_PATH.insert(0, projectDir + '/media/templates/')

app = Bottle()
filesTable = Files()

@app.route('/')
@view('index')
def index(appName="HandleBar"):
	bottle.TEMPLATES.clear()
	
	fileList = filesTable.list()
	
	return dict(appName=appName, list=fileList)
	
@app.route('/clear')
def clearDb():
	ci = request.query.c
	
	if ci == "imsure":
		filesTable.clearDb()
		
	redirect("/")

@app.route('/retry')
def retry():
	
	media = []
	
	for root, dirs, files in os.walk(projectDir + DebugFailedPath):
		for files in ['*.m4v']:
			fp = root + '/' + files
			media.extend(glob.glob(fp))
			
	for path in media:
		newFilename = os.path.basename(fp)
		
		md = metadata(path, 0)
		result = md.parseFile()
		
		if result != True:
			os.rename(path, HandleBarConfigPath + DebugFailedPath + '/' + newFilename)
			return False
		
		moveToItunes(md.filePath)
	
	redirect("/failed")
	
@app.route('/log')
@view('log')
def log(appName="HandleBar"):
	bottle.TEMPLATES.clear()
	
	data_file = open('/tmp/handleBarError.log', 'r')
	log = data_file.readlines()[-200:]  
    	
	return dict(appName=appName, outLog=log)

@app.route('/failed')
@view('failed')
def log(appName="HandleBar"):
	bottle.TEMPLATES.clear()
	
	list = os.listdir(projectDir + DebugFailedPath) 
    	
	return dict(appName=appName, failedFiles=list)
		
@app.route('/progress')
def progress():
	
	hb = os.system('ps ax | grep -v grep | grep HandBrakeCLI > /dev/null');
	
	if hb == 0:
		with open("/tmp/handleBarEncode.status") as f:
		    line = f.readline()
		
		log = line.rsplit('\r')[-1]
		   	
		return log
	else:
		return "none"
	
@app.route('/media/<filepath:path>')
def static(filepath):
	return static_file(filepath, root=projectDir + '/media/')

host = socket.gethostbyname(socket.gethostname())

run(app, host=host, port=8082, reloader=True)