import os, subliminal

class subs:
        
        def __init__(self, file):
 
        	self.filePath = file
        	       	
        def downloadSubtitles(self):

	        cwd = os.path.abspath(os.path.dirname(self.filePath)) + '/../subtitles'
	        os.chdir(cwd)	        	        
	        #os.rename(self.filePath, cwd + '1/'+ os.path.basename(self.filePath))
	        
	        sub = subliminal.download_subtitles(os.path.basename(self.filePath), ['nl'], cache_dir="/tmp")
	        print sub       	
