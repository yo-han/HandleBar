""" 
HandleBar
"""

import os, sys
import guessit
import requests
import tmdb
import tvdb_api
from pync import Notifier

class movieData:
	
	def __init__(self, title):
		
		self.movieTitle = title
		self.movieImage = ""
		self.movieName = ""		        	
		self.movieDescription = ""
		self.movieRating = ""
		self.movieReleased = ""
		self.movieDirector = ""
		self.movieGenre = ""
					
	def getMovie(self):
		
		#try:
			results = tmdb.search(self.movieTitle)
			
			if not results:
				return False
			
			movie = tmdb.getMovieInfo(results[0]['id'])
			
			""" What to expect """
			#print movie.keys()
						
			self.movieImage = self.setImage(movie['images'][0])
			self.movieName = movie['name']
			self.movieDescription = movie['overview']
			self.movieRating = movie['rating']
			self.movieReleased = movie['released']
			self.movieDirector = movie['cast']['director'][0]['name']
			self.movieGenre = movie['categories']['genre'].keys()[0]
						
			return self
			
		#except:
		#	print "Unexpected error:", sys.exc_info()[0]
		#	return False
			
	def setImage(self, images):
		
		for key in images.keys():
			
			if key == 'original':
				return images[key]
			elif key == 'cover':
				return images[key]
			else:
				pass
				
class tvData:
	
	def __init__(self, serieData):
		
		self.seriesTitle = serieData['series']
		self.seriesSeason = ""
		self.seriesEpisode = ""
		self.seriesEpisodeName = ""
		self.seriesDescription = ""
		self.seriesRating = ""
		self.seriesAirDate = ""
		self.seriesNetwork = ""
		self.seriesGenre = ""
		self.seriesImage = ""
		
		if "season" in serieData:
						
			self.seriesSeason = serieData['season']
			self.seriesEpisode = serieData['episodeNumber']	        	

					
	def getEpisode(self):
		
		if self.seriesSeason == "":
			return self
			
		tvdb = tvdb_api.Tvdb(banners=True)
		for s in tvdb[self.seriesTitle]['_banners']['season']['season']:
			artwork = tvdb[self.seriesTitle]['_banners']['season']['season'][s]
			
			if artwork['language'] == "en" and int(artwork['season']) == int(self.seriesSeason):
				self.seriesImage = artwork['_bannerpath']
				break 
		
		self.seriesTitle  = tvdb[self.seriesTitle]['seriesname']
		self.seriesEpisodeName  = tvdb[self.seriesTitle][int(self.seriesSeason)][int(self.seriesEpisode)]['episodename']
		self.seriesDescription  = tvdb[self.seriesTitle][int(self.seriesSeason)][int(self.seriesEpisode)]['overview']
		self.seriesRating  = tvdb[self.seriesTitle]['contentrating']
		self.seriesAirDate = tvdb[self.seriesTitle][int(self.seriesSeason)][int(self.seriesEpisode)]['firstaired']
		self.seriesNetwork = tvdb[self.seriesTitle]['network']
		
		self.seriesGenre = (tvdb[self.seriesTitle]['genre'])[1:len(tvdb[self.seriesTitle]['genre'])]
		self.seriesGenre = self.seriesGenre[0:self.seriesGenre.find("|")]
		
		return self
				
class metadata:
        """
        A generic daemon class.
       
        Usage: subclass the Daemon class and override the run() method
        """
        def __init__(self, file):
 
        	self.filePath = file
        	self.projectPath = os.getcwd()
        	self.AtomicParsleyPath = self.projectPath + "/bin/AtomicParsley"
       	
        def parseFile(self):
	   
        	guess = guessit.guess_video_info(self.filePath, info = ['filename'])
       		self.setMetaData(guess)
        
        def setMetaData(self, guess):
        
        	hd = ""
        	
        	if "screenSize" in guess and (guess['screenSize'] == '720p' or guess['screenSize'] == '1080p'):
        		hd = ' --meta-uuid "hdvd" true'

			if guess['type'] == "movie":
				
				mvd = movieData(guess['title'])
				data = mvd.getMovie()
				
				artwork = ""
				
				image = self.downloadImage(data.movieImage)     
				if image is not "":
					artwork = '--artwork "' + image + '"'
					
				Notifier.notify('Movie: ' + data.movieName, group=os.getpid(), title='HandleBar: Set metadata')
				
				os.system(self.AtomicParsleyPath + ' ' + self.filePath + ' --overWrite ' + artwork + ' --title "' + data.movieName + '" --artist "' + data.movieDirector +  '" --genre "' + data.movieGenre + '" --year ' + data.movieReleased + ' --description "' + data.movieDescription + '" --advisory "' + data.movieRating + '" --stik "Normal" --comment "Mustacherioused"' + hd)
				
				if image is not "":
					os.remove(image)
				
			elif guess['type'] == "episode":
			
				tvd = tvData(guess)
				data = tvd.getEpisode()
				
				artwork = ""
				title = ""
				
				image = self.downloadImage(data.seriesImage)    
				if image is not "":
					artwork = '--artwork "' + image + '"'			
				
				if data.seriesTitle.find('revolution.') != -1:
					title = data.seriesTitle[:-5]
				elif data.seriesTitle == 'vegas':
					title = data.seriesTitle  + " (2012)"
				else:
					title = data.seriesTitle
				
				Notifier.notify('TV Show: ' + title, group=os.getpid(), title='HandleBar: Set metadata')
							
				#os.system(self.AtomicParsleyPath + ' ' + self.filePath + ' --artwork REMOVE_ALL')
				os.system(self.AtomicParsleyPath + ' ' + self.filePath + ' --overWrite ' + artwork + ' --TVShowName "' + title + '" --TVSeasonNum "' + str(data.seriesSeason) +  '" --TVEpisodeNum "' + str(data.seriesEpisode) + '" --TVNetwork "' + str(data.seriesNetwork) + '" --title "' + data.seriesEpisodeName + '" --description "' + data.seriesDescription + '" --advisory "' + data.seriesRating + '" --year "' + data.seriesAirDate + '" --genre "' + data.seriesGenre + '" --track "' + str(data.seriesEpisode) + '" --disk  "' + str(data.seriesSeason) + '" --stik "TV Show" --comment "Mustacherioused"' + hd)
				
				if image is not "":
					os.remove(image)
			
			Notifier.notify('Copy to iTunes', group=os.getpid(), title='HandleBar')
			
			os.system("osascript -e 'tell application \"iTunes\" to add POSIX file \"" + self.filePath + "\"'")
			os.remove(self.filePath)
			
			return True
        	
        def downloadImage(self, url):
        	
        	path = self.projectPath + '/media/' + os.path.basename(url)
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

        		
if __name__ == "__main__":    
	md = metadata("/Users/johan/Documents/ProjectX/media/ready/episode/family.guy.S11E07.1080.m4v")
	md.parseFile()