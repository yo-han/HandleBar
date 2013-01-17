import os, sys, glob, time, guessit

from lib import *
from app import *

projectDir = HandleBarConfigPath

class metadata:
        """
        A generic daemon class.
       
        Usage: subclass the Daemon class and override the run() method
        """
        def __init__(self, file, fileId):
 
        	self.filePath = file
        	self.fileId = fileId
        	self.AtomicParsleyPath = projectDir + "/bin/AtomicParsley"
        	       	
        def parseFile(self):
	   
        	guess = guessit.guess_video_info(self.filePath, info = ['filename'])
        	
        	return self.setMetaData(guess)
        
        def setMetaData(self, guess):
               	        	       	
            if "screenSize" in guess and (guess['screenSize'] == '720p' or guess['screenSize'] == '1080p'):
            	hd = ['--meta-uuid','hdvd','true']
            else:
            	hd = []
   	        	       	
            if guess['type'] == "movie":
				
            	print "Movie"
					
            	mvd = movie(guess['title'])

            	if mvd.foundMovie == False:
            		Notify('No data found for this movie', 'HandleBar: Error')
            		return False
					
            	artwork = []
				
            	image = self.downloadImage(mvd.getImage())     
            	if image is not "":
            		artwork = ['--artwork',image]
					
            	Notify('Movie: ' + mvd.getName(), 'HandleBar: Set metadata')
				
            	#subprocess.call([self.AtomicParsleyPath, self.filePath, '--artwork','REMOVE_ALL']);
            	#os.system(self.AtomicParsleyPath + ' ' + self.filePath + ' --overWrite  --title "' + data.movieName + '" --artist "' + data.movieDirector +  '" --genre "' + data.movieGenre + '" --year ' + data.movieReleased + ' --description "' + data.movieDescription + '" --advisory "' + data.movieRating + '" --stik "Short Film" --comment "Mustacherioused"')
            	           	      	
            	alist = [self.AtomicParsleyPath, self.filePath, '--overWrite','--title',mvd.getName(),'--artist',mvd.getDirector(),'--genre',mvd.getGenre(),'--year',mvd.getReleased(),'--description',mvd.getDescription(),'--advisory',mvd.getRating(),'--stik','Short Film','--comment','Mustacherioused']
            	arguments = alist + artwork + hd
				
            	logATP = open("/tmp/atomicParsley.log", "a")
            	subprocess.call(arguments, shell=False, stdout=logATP, stderr=subprocess.STDOUT)
				
            	filesTable.movie(self.fileId, mvd.getName(), os.path.basename(image), mvd.getDirector(), mvd.getGenre(), mvd.getReleased(), mvd.getDescription(), mvd.getRating(), mvd.getImdbid(), hd)
				
            	return True
							
            elif guess['type'] == "episode":
				
            	print "TV Show"
				
            	episode = tvEpisode(guess)

            	if episode.foundSeries == False:
            		Notify('No data found for this episode', 'HandleBar: Error')
            		return False
            		
            	artwork = []
            	title = episode.getTitleClean()

            	image = self.downloadImage(episode.getImage())    
            	if image is not "":
            		artwork = ['--artwork',image]
           					
            	Notify('TV Show: ' + title, 'HandleBar: Set metadata')
				
            	alist = [self.AtomicParsleyPath, self.filePath, '--overWrite','--TVShowName',title,'--TVSeasonNum',episode.getSeason(),'--TVEpisodeNum',episode.getEpisode(),'--TVNetwork',episode.getNetwork(),'--title',episode.getEpisodeName(),'--description',episode.getDescription(),'--advisory',episode.getRating(),'--year',episode.getAirdate(),'--genre',episode.getGenre(),'--track',episode.getEpisode(),'--disk',episode.getSeason(),'--stik','TV Show','--comment','Mustacherioused']
            	arguments = alist + artwork + hd
				
            	logATP = open("/tmp/atomicParsley.log", "a")
            	subprocess.call(arguments, shell=False, stdout=logATP, stderr=subprocess.STDOUT)
				
            	filesTable.episode(self.fileId, title, os.path.basename(image), episode.getSeason(), episode.getEpisode(), episode.getNetwork(), episode.getEpisodeName(), episode.getDescription(), episode.getRating(), episode.getAirdate(), episode.getGenre(), hd)
				
            	return True
            else:
            	print "Unknown type"
            	return False										
			
        	
        def downloadImage(self, url):
        	
        	path = projectDir + 'media/images/' + os.path.basename(url)
        	downloaded = False
        	
        	for i in range(0,5):
        		try:
        			r = requests.get(url, timeout=1)
		        	if r.status_code == 200:
			        	with open(path, 'wb') as f:
			        		for chunk in r.iter_content():
			        			f.write(chunk)
			        downloaded = True
			        break
        		except:
        			continue
        		break
   	        
   	        if downloaded == True:
		        return path

	    	return ""