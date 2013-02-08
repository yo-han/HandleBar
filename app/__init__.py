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
							
	os.remove(file)
	
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
			print "FAILED --"
			return False
		
		moveToItunes(md.filePath)
		
def reSub():
	
	media = []
	
	import popen2
	import enzyme

	for mediaPath in ReSubSearchPaths:
		for root, dirs, files in os.walk(mediaPath):
			for files in ['*.m4v']:
				fp = root + '/' + files
				print fp
				media.extend(glob.glob(fp))
			
	for path in media:
 		
		r = popen2.popen3(HandleBarConfigPath + 'bin/SublerCLI -source "' + path + '" -listtracks')
		tracks = r[0].readlines()
		r[0].close()
				
		subsInTrack = filter(hasSubtitle, tracks)
		if len(subsInTrack) > 0:
			continue
			
		r = popen2.popen3(HandleBarConfigPath + 'bin/SublerCLI -source "' + path + '" -listmetadata')
		comments = r[0].readlines()
		matches = filter(hasComments, comments)
		
		if len(matches) > 0:
			
			start = len('Comments: Original filename ')
			file = matches[0][start:].strip()
			
			md = metadata(file, 0)
			print file
			sub = subs(file, md.guess['type'])
			sub.downloadSubtitles()
			
		
def hasComments(f):
	if f.find('Comments: Original filename') > -1:
		return True
	return False
	
def hasSubtitle(f):
	if f.find('Subtitle Track') > -1:
		return True
	return False
	
""" Logger (not in use, but can be used for debugging purposes """
log = Logger('HandleBar')

""" Files db """
filesTable = Files()

from tv import *
from movie import *		
from metadata import *
from subs import *
