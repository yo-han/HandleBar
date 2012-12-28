""" 
HandleBar
"""

import os, sys, glob, time, guessit
from lib import *
from app import *

def Notify(message, title):
	if NotificationOn:
		Notifier.notify(message, group=os.getpid(), title=title)

projectDir = os.path.abspath(os.path.dirname(__file__))

""" Logger (not in use, but can be used for debugging purposes """
log = Logger('HandleBar')

""" Files db """
filesTable = Files()
	
class hbHandle(object):
    
    def __init__(self):
		return None
		               
    def check(self):

    	files = []
    	
    	for path in MediaPaths:
    		files.extend(self.findRawMedia(path))
    	
    	if not files:
    		
    		if not DebugMode:
    			return False
    		else:
    			Notify('No files found',"HandleBar")
    			
    	else:
    		newFilepath = os.path.splitext(files[0])[0] + '.m4v'
    		oldFilepath = files[0]
    		newFilename = os.path.basename(newFilepath)
    		oldFilename = os.path.basename(files[0])
    		
    		guess = guessit.guess_video_info(oldFilepath, info = ['filename'])
    		type = guess['type']
    		
    		fileId = filesTable.new(type, oldFilename)
    		
    		if not fileId:
    			Notify('Insert of new file record failed', 'HandleBar: Error')
    			return False
    		
    		Notify('File: ' + oldFilename, 'HandleBar: Start converting ' + type)
    		
    		os.system('nice -n 20 ' + HandbrakeCLIPath + ' -i "' + oldFilepath + '" -o "' + newFilepath + '" --large-file --preset "' + HandBrakePreset + '" --native-language "' + HandBrakeLanguage + '"')    
    		
    		filesTable.convertDone(fileId)
    		
    		Notifier.notify('File: ' + oldFilename, group=os.getpid(), title='HandleBar: Convert done')

    		if DebugMode:
    			os.rename(oldFilepath, DebugRemovePath + '/' + oldFilename)
    		else:
    			os.remove(oldFilepath)
    		
    		Notify('File: ' + oldFilename, 'HandleBar: Parse metadata')
    		
    		md = metadata(newFilepath, fileId)
    		md.parseFile()
    		
    		Notify('Copy to iTunes', 'HandleBar')
    		
    		os.system("osascript -e 'tell application \"iTunes\" to add POSIX file \"" + md.filePath + "\"'")
    		os.remove(md.filePath)

    	return True
    		
    def findRawMedia(self, path):	

    	media = []
    	
    	for root, dirs, files in os.walk(path):
    		for files in FileTypes:
    			media.extend(glob.glob(root + '/' + files))
    	
    	return media   			  

class movie:
	
	def __init__(self, title):
		
		self.movieTitle = title
		self.movieImage = ""
		self.movieName = ""		        	
		self.movieDescription = ""
		self.movieRating = ""
		self.movieReleased = ""
		self.movieDirector = ""
		self.movieGenre = ""
		self.imdbId = ""
					
	def getMovie(self):
		
		#try:
			results = tmdb.search(self.movieTitle)
			
			if not results:
				return False
			
			movie = tmdb.getMovieInfo(results[0]['id'])
			
			""" What to expect """
			print movie.keys()
						
			self.movieImage = self.setImage(movie['images'][0])
			self.movieName = movie['name']
			self.movieDescription = movie['overview']
			self.movieRating = movie['rating']
			self.movieReleased = movie['released']
			self.movieDirector = movie['cast']['director'][0]['name']
			self.movieGenre = movie['categories']['genre'].keys()[0]
			self.imdbId = movie['imdb_id']
						
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
				
class tvEpisode:
	
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
        def __init__(self, file, fileId):
 
        	self.filePath = file
        	self.fileId = fileId
        	self.AtomicParsleyPath = projectDir + "/bin/AtomicParsley"
       	
        def parseFile(self):
	   
        	guess = guessit.guess_video_info(self.filePath, info = ['filename'])
       		self.setMetaData(guess)
        
        def setMetaData(self, guess):
        	
        	hd = ""
        	
        	if "screenSize" in guess and (guess['screenSize'] == '720p' or guess['screenSize'] == '1080p'):
        		hd = ' --meta-uuid "hdvd" true'

			if guess['type'] == "movie":
				
				mvd = movie(guess['title'])
				data = mvd.getMovie()
			
				if not data:
					Notify('No data found for this movie', 'HandleBar: Error')
					return False
					
				artwork = ""

				image = self.downloadImage(data.movieImage)     
				if image is not "":
					artwork = '--artwork "' + image + '"'
					
				Notify('Movie: ' + data.movieName, 'HandleBar: Set metadata')
				
				os.system(self.AtomicParsleyPath + ' ' + self.filePath + ' --overWrite ' + artwork + ' --title "' + data.movieName + '" --artist "' + data.movieDirector +  '" --genre "' + data.movieGenre + '" --year ' + data.movieReleased + ' --description "' + data.movieDescription + '" --advisory "' + data.movieRating + '" --stik "Short Film" --comment "Mustacherioused"' + hd)
				
				filesTable.movie(self.fileId, data.movieName, os.path.basename(image), data.movieDirector, data.movieGenre, data.movieReleased, data.movieDescription, data.movieRating, data.imdbId, hd)
				
			elif guess['type'] == "episode":
			
				episode = tvEpisode(guess)
				data = episode.getEpisode()
				
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
				
				Notify('TV Show: ' + title, 'HandleBar: Set metadata')
							
				os.system(self.AtomicParsleyPath + ' ' + self.filePath + ' --overWrite ' + artwork + ' --TVShowName "' + title + '" --TVSeasonNum "' + str(data.seriesSeason) +  '" --TVEpisodeNum "' + str(data.seriesEpisode) + '" --TVNetwork "' + str(data.seriesNetwork) + '" --title "' + data.seriesEpisodeName + '" --description "' + data.seriesDescription + '" --advisory "' + data.seriesRating + '" --year "' + data.seriesAirDate + '" --genre "' + data.seriesGenre + '" --track "' + str(data.seriesEpisode) + '" --disk  "' + str(data.seriesSeason) + '" --stik "TV Show" --comment "Mustacherioused"' + hd)
				
				filesTable.episode(self.fileId, title, os.path.basename(image), data.seriesSeason, data.seriesEpisode, data.seriesNetwork, data.seriesEpisodeName, data.seriesDescription, data.seriesRating, data.seriesAirDate, data.seriesGenre, hd)
									
			return True
        	
        def downloadImage(self, url):
        	
        	path = projectDir + '/media/images/' + os.path.basename(url)
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