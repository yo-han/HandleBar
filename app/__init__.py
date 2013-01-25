from logger import Logger
from config import *
from database import *

def Notify(message, title):
	if NotificationOn:
		Notifier.notify(message, group=os.getpid(), title=title)
		
	updateConvertStatus(message)
	
def updateConvertStatus(status):
	f = open('/tmp/handleBarCurrentStatus', 'w')
	f.write(status)
	f.close()

def moveToItunes(file):
	
	Notify('Copy to iTunes', 'HandleBar')
	os.system("""osascript << EOF
				tell application "iTunes"
				    launch
				    with timeout of 30000 seconds
				        add ("%s" as POSIX file)
				    end timeout
				end tell
				EOF""" % file)
							
	#os.remove(file)
	
def parseFailedFiles():
	
	media = []
	
	for root, dirs, files in os.walk(HandleBarConfigPath + DebugFailedPath):
		for files in ['*.m4v']:
			fp = root + '/' + files
			media.extend(glob.glob(fp))
			
	for path in media:
		  		
		md = metadata(path, 0)
		
		""" SUBS """
   		sub = subs(path, md.guess['type'])
   		sub.downloadSubtitles()
   		
		result = md.parseFile()
		
		if result != True:
			return False
		
		moveToItunes(md.filePath)
		
""" Logger (not in use, but can be used for debugging purposes """
log = Logger('HandleBar')

""" Files db """
filesTable = Files()

from tv import *
from movie import *		
from metadata import *
from subs import *
