""" 
HandleBar
"""

import os, sys, glob, time, logging
import guessit
from daemon import Daemon
from logger import Logger 
from metadata import metadata
from pync import Notifier

op = os.path
log = Logger('HandleBar')

class hbHandle(object):
    
    def __init__(self):
    
    	self.projectPath = os.path.dirname( __file__ )
        self.hbPath = self.projectPath + "/bin/HandBrakeCLI"
        self.readyPath = self.projectPath + "/media/ready"
        self.removedPath = self.projectPath + "/media/done"
        self.mediaPaths = ("/Users/johan/Documents/HandleBar/media/tv", "/Users/johan/Documents/HandleBar/media/movies")
        self.fileTypes = ('*.mov', '*.mkv', '*.avi', '*.m2ts', '*.mp4', '*.iso', '*.mpg')
        self.hbPreset = "AppleTV 3"
        self.hbLanguage = "nld,eng"
               
    def check(self):

    	files = []
    	
    	for path in self.mediaPaths:
    		files.extend(self.findRawMedia(path))
    	
    	if not files:
    		return False
    		#Notifier.notify('No files found', group=os.getpid(), title="HandleBar")
    	else:
    		newFilepath = os.path.splitext(files[0])[0] + '.m4v'
    		oldFilepath = files[0]
    		newFilename = os.path.basename(newFilepath)
    		oldFilename = os.path.basename(files[0])
    		
    		guess = guessit.guess_video_info(oldFilepath, info = ['filename'])
    		type = guess['type']
    		
    		Notifier.notify('File: ' + oldFilename, group=os.getpid(), title='HandleBar: Start converting ' + type)
    		
    		os.system('nice -n 20 ' + self.hbPath + ' -i "' + oldFilepath + '" -o "' + newFilepath + '" --large-file --preset "' + self.hbPreset + '" --native-language "' + self.hbLanguage + '"')    		    		    
    		
    		Notifier.notify('File: ' + oldFilename, group=os.getpid(), title='HandleBar: Convert done')
    		
    		os.rename(oldFilepath, self.removedPath + '/' + oldFilename)
    		#os.remove(oldFilepath)
    		os.rename(newFilepath, self.readyPath + '/' + type + '/' + newFilename)
    		
    		Notifier.notify('File: ' + oldFilename, group=os.getpid(), title='HandleBar: Parse metadata')
    		
    		md = metadata(self.readyPath + '/' + type + '/' + newFilename)
    		md.parseFile()

    	return True
    		
    def findRawMedia(self, path):	

    	media = []
    	
    	for root, dirs, files in os.walk(path):
    		for files in self.fileTypes:
    			media.extend(glob.glob(root + '/' + files))
    	
    	return media   			  

hb = hbHandle();

class ConvertDaemon(Daemon):
	def run(self):
		while True:
			
			"""
			Ain't necessary no more
			running = os.system("ps ax | grep -v grep | grep " + hb.hbPath + " > /dev/null") 
			log.lg.info(running)
			"""
			time.sleep(5)
			hb.check()
        	 
if __name__ == "__main__":
	daemon = ConvertDaemon('/tmp/convert-daemon.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'test' == sys.argv[1]:
			hb.check()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|test" % sys.argv[0]
        sys.exit(2)
