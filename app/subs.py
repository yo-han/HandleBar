import os, subliminal

from app import *

projectDir = HandleBarConfigPath

class subs:
        
        def __init__(self, file):
 
        	self.filePath = file
        	       	
        def downloadSubtitles(self):

	        cwd = os.path.abspath(projectDir + SubtitlePath)
	        os.chdir(cwd)	        	        
	        	        
	        sub = subliminal.download_subtitles(os.path.basename(self.filePath), ['nl'], cache_dir="/tmp")
	        #print sub       	