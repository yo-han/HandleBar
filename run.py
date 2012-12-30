import os, socket, sys, subprocess, signal, time

sysArgv = None

if vars().has_key('NSFile'):
	__file__ = NSFile

pidFileServer = '/tmp/handleBarServer.pid'

projectDir = os.path.abspath(os.path.dirname(__file__))
host = socket.gethostbyname(socket.gethostname())
currentHost = "http://" + host + ":8082"

class runHandleBar(object):
	
	def __init__(self):
		return None
	
	def kill(self, pidFile):
		
		# Get the pid from the pidfile
		try:
		    pf = file(pidFile,'r')
		    pid = int(pf.read().strip())
		    pf.close()
		except IOError:
		    pid = None
		
		if pid:
		    # Try killing the daemon process
		    try:
		        while 1:
		            os.kill(pid, signal.SIGKILL)
		            time.sleep(0.1)
		    except OSError, err:
		        error = None
		        
	def pid(self, pid, pidFile):
	    f = open(pidFile, 'w')
	    f.write(pid)
	    f.close()

	def start(self):
		p = subprocess.Popen(['python', projectDir + '/view.py'])
		self.pid(str(p.pid), pidFileServer)
		
		subprocess.Popen(['python', projectDir + '/convert.py', 'start'])
		
handleBar = runHandleBar()

handleBar.start()	