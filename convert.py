""" 
HandleBar
"""

import os, sys, glob, time, guessit
from lib import *
from app import *

projectDir = os.path.abspath(os.path.dirname(__file__))

class hbHandle(object):
    
    def __init__(self):
    	return None
		               
    def check(self):

    	files = []
    	
    	for path in MediaPaths:
    		files.extend(self.findRawMedia(path))
    	
    	if not files:
    		
    		print "No files found"	
    		    			
    	else:
    		newFilepath = os.path.splitext(files[0])[0] + '.m4v'
    		oldFilepath = files[0]
    		newFilename = os.path.basename(newFilepath)
    		oldFilename = os.path.basename(files[0])
    		
    		guess = guessit.guess_video_info(oldFilepath, info = ['filename'])
    		type = guess['type']
    		   		
    		fileId = filesTable.new(type, oldFilename)
    		
    		""" Metadata testing """
    		"""
    		md = metadata(oldFilepath, fileId)
    		result = md.parseFile()
    		print result
    		sys.exit(0)"""
    	    		
    		if not fileId:
    			Notify('Insert of new file record failed', 'HandleBar: Error')
    			return False
    		
    		Notify('File: ' + oldFilename, 'HandleBar: Start converting ' + type)
    		
    		os.system('nice -n 20 ' + HandbrakeCLIPath + ' -i "' + oldFilepath + '" -o "' + newFilepath + '" --preset "' + HandBrakePreset + '" --native-language "' + HandBrakeLanguage + '" --native-dub 1> /tmp/handleBarEncode.status')    
    		
    		try:
    			with open(newFilepath) as f: pass
    		except IOError as e:
    			os.rename(oldFilepath, HandleBarConfigPath + DebugFailedPath + '/' + oldFilename)
    			return False
    			
    		filesTable.convertDone(fileId)
    		
    		Notifier.notify('File: ' + oldFilename, group=os.getpid(), title='HandleBar: Convert done')

    		if DebugMode:
    			os.rename(oldFilepath, HandleBarConfigPath + DebugRemovePath + '/' + oldFilename)
    		else:
    			os.remove(oldFilepath)
    		
    		Notify('File: ' + oldFilename, 'HandleBar: Parse metadata')
    		
    		convertedPath = HandleBarConfigPath + ReadyPath + '/' + newFilename
    		
    		os.rename(newFilepath, convertedPath)
    		
    		md = metadata(convertedPath, fileId)
    		result = md.parseFile()
    		
    		if result != True:
    			os.rename(convertedPath, HandleBarConfigPath + DebugFailedPath + '/' + newFilename)
    			return False
    		
    		moveToItunes(md.filePath)
    		    		
    	return True
    		
    def findRawMedia(self, path):	

    	media = []
    	
    	for root, dirs, files in os.walk(path):
    		for files in FileTypes:
    			fp = root + '/' + files
    			
    			if fp.find('_UNPACK_') < 0:
    				media.extend(glob.glob(fp))
    	
    	return media   			  
    	
hb = hbHandle();

class ConvertDaemon(Daemon):
	def run(self):
		while True:
			
			"""
			log.lg.info("Run forest, run")
			"""

			time.sleep(5)
			hb.check()
        	 
if __name__ == "__main__":

	daemon = ConvertDaemon('/tmp/convert-daemon.pid', '/dev/null', '/tmp/handleBarOut.log', '/tmp/handleBarError.log')
	
	if len(sys.argv) >= 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'test' == sys.argv[1]:
			hb.check()
		elif 'metatest' == sys.argv[1]:
			md = metadata(sys.argv[2], 1)
			result = md.parseFile()
			sys.exit(0)
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|test" % sys.argv[0]
        sys.exit(2)