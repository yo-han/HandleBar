import os, subliminal

from app import *

projectDir = HandleBarConfigPath

class subs:
        
        def __init__(self, file, type):
 
        	self.filePath = file

        	if type == "movie":
        		self.services = ['addic7ed', 'opensubtitles', 'subswiki', 'thesubdb']
        	else:
        		self.services = ['bierdopje']
        	
        	       	
        def downloadSubtitles(self):

	        cwd = os.path.abspath(projectDir + '/' + SubtitlePath)
	        os.chdir(cwd)	        	        

	        sub = subliminal.download_subtitles(os.path.basename(self.filePath), ['nl'], cache_dir="/tmp", services=self.services)
	        #print sub       	
