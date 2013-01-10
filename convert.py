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
    		
    		os.system('nice -n 20 ' + HandbrakeCLIPath + ' -i "' + oldFilepath + '" -o "' + newFilepath + '" --large-file --preset "' + HandBrakePreset + '" --native-language "' + HandBrakeLanguage + '" --native-dub')    
    		
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
    		
    		md = metadata(newFilepath, fileId)
    		result = md.parseFile()
    		
    		if result != True:
    			os.rename(newFilepath, HandleBarConfigPath + DebugFailedPath + '/' + newFilename)
    			return False
    		
    		Notify('Copy to iTunes', 'HandleBar')
    		    		
    		#os.system("osascript -e 'tell application \"iTunes\"  to add POSIX file \"" + md.filePath + "\"'")
    		os.system("""osascript << EOF
						tell application "iTunes"
						    launch
						    with timeout of 30000 seconds
						        add ("%s" as POSIX file)
						    end timeout
						end tell
						EOF""" % md.filePath)
    		os.remove(md.filePath)

    	return True
    		
    def findRawMedia(self, path):	

    	media = []
    	
    	for root, dirs, files in os.walk(path):
    		for files in FileTypes:
    			fp = root + '/' + files
    			
    			if fp.find('_UNPACK_') < 0:
    				media.extend(glob.glob(fp))
    	
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
			self.movieName = movie['name'].encode('utf-8').strip()
			self.movieDescription = movie['overview'].encode('utf-8').strip()
			self.movieRating = movie['rating'].encode('utf-8').strip()
			self.movieReleased = movie['released']
			self.movieDirector = movie['cast']['director'][0]['name'].encode('utf-8').strip()
			self.movieGenre = movie['categories']['genre'].keys()[0].encode('utf-8').strip()
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
		
		self.seriesTitle = serieData['series'].encode('utf-8').strip()
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
		print tvdb[self.seriesTitle]
		self.seriesTitle  = tvdb[self.seriesTitle]['seriesname'].encode('utf-8').strip()
		self.seriesEpisodeName  = tvdb[self.seriesTitle][int(self.seriesSeason)][int(self.seriesEpisode)]['episodename'].encode('utf-8').strip()
		self.seriesDescription  = tvdb[self.seriesTitle][int(self.seriesSeason)][int(self.seriesEpisode)]['overview'].encode('utf-8').strip()
		self.seriesAirDate = tvdb[self.seriesTitle][int(self.seriesSeason)][int(self.seriesEpisode)]['firstaired'].encode('utf-8').strip()
		self.seriesNetwork = tvdb[self.seriesTitle]['network'].encode('utf-8').strip()
		
		self.seriesGenre = (tvdb[self.seriesTitle]['genre'])[1:len(tvdb[self.seriesTitle]['genre'])]
		self.seriesGenre = self.seriesGenre[0:self.seriesGenre.find("|")].encode('utf-8').strip()
		
		if tvdb[self.seriesTitle]['contentrating'] is not None:
			self.seriesRating  = tvdb[self.seriesTitle]['contentrating'].encode('utf-8').strip()
		
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
        	
        	return self.setMetaData(guess)
        
        def setMetaData(self, guess):
               	        	       	
            if "screenSize" in guess and (guess['screenSize'] == '720p' or guess['screenSize'] == '1080p'):
            	hd = ['--meta-uuid','hdvd','true']
            else:
            	hd = []
   	        	       	
            if guess['type'] == "movie":
				
            	print "Movie"
					
            	mvd = movie(guess['title'])
            	data = mvd.getMovie()

            	if not data:
            		Notify('No data found for this movie', 'HandleBar: Error')
            		return False
					
            	artwork = []
				
            	image = self.downloadImage(data.movieImage)     
            	if image is not "":
            		artwork = ['--artwork',image]
					
            	Notify('Movie: ' + data.movieName, 'HandleBar: Set metadata')
				
            	#os.system(self.AtomicParsleyPath + ' ' + self.filePath + ' --overWrite ' + artwork + ' --title "' + data.movieName + '" --artist "' + data.movieDirector +  '" --genre "' + data.movieGenre + '" --year ' + data.movieReleased + ' --description "' + data.movieDescription + '" --advisory "' + data.movieRating + '" --stik "Short Film" --comment "Mustacherioused"' + hd)
            	subprocess.call([self.AtomicParsleyPath, self.filePath, '--artwork','REMOVE_ALL']);
            	
            	alist = [self.AtomicParsleyPath, self.filePath, '--overWrite','--title',data.movieName,'--artist',data.movieDirector,'--genre',data.movieGenre,'--year',data.movieReleased,'--description',data.movieDescription,'--advisory',data.movieRating,'--stik','Short Film','--comment','Mustacherioused']
            	arguments = alist + artwork + hd
				
            	subprocess.call(arguments, shell = False)
				
            	filesTable.movie(self.fileId, data.movieName, os.path.basename(image), data.movieDirector, data.movieGenre, data.movieReleased, data.movieDescription, data.movieRating, data.imdbId, hd)
				
            	return True
							
            elif guess['type'] == "episode":
				
            	print "TV Show"
				
            	episode = tvEpisode(guess)
            	data = episode.getEpisode()
				
            	artwork = []
            	title = ""
				
            	image = self.downloadImage(data.seriesImage)    
            	if image is not "":
            		artwork = ['--artwork',image]
				
            	if data.seriesTitle.find('revolution.') != -1:
            		title = data.seriesTitle[:-5]
            	elif data.seriesTitle == 'vegas':
            		title = data.seriesTitle  + " (2012)"
            	else:
            		title = data.seriesTitle
				
            	Notify('TV Show: ' + title, 'HandleBar: Set metadata')
							
            	#os.system(self.AtomicParsleyPath + ' ' + self.filePath + ' --overWrite ' + artwork + ' --TVShowName "' + title + '" --TVSeasonNum "' + str(data.seriesSeason) +  '" --TVEpisodeNum "' + str(data.seriesEpisode) + '" --TVNetwork "' + str(data.seriesNetwork) + '" --title "' + data.seriesEpisodeName + '" --description "' + data.seriesDescription + '" --advisory "' + data.seriesRating + '" --year "' + data.seriesAirDate + '" --genre "' + data.seriesGenre + '" --track "' + str(data.seriesEpisode) + '" --disk  "' + str(data.seriesSeason) + '" --stik "TV Show" --comment "Mustacherioused"' + hd)
				
            	alist = [self.AtomicParsleyPath, self.filePath, '--overWrite','--TVShowName',title,'--TVSeasonNum',str(data.seriesSeason),'--TVEpisodeNum',str(data.seriesEpisode),'--TVNetwork',str(data.seriesNetwork),'--title',data.seriesEpisodeName,'--description',data.seriesDescription,'--advisory',data.seriesRating,'--year',data.seriesAirDate,'--genre',data.seriesGenre,'--track',str(data.seriesEpisode),'--disk',str(data.seriesSeason),'--stik','TV Show','--comment','Mustacherioused']
            	arguments = alist + artwork + hd
				
            	subprocess.call(arguments, shell = False)
				
            	filesTable.episode(self.fileId, title, os.path.basename(image), data.seriesSeason, data.seriesEpisode, data.seriesNetwork, data.seriesEpisodeName, data.seriesDescription, data.seriesRating, data.seriesAirDate, data.seriesGenre, hd)
				
            	return True
            else:
            	print "Unknown type"
            	return False										
			
        	
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
			print "----> " + os.system('ps ax | grep -v grep | grep HandBrakeCLI > /dev/null');
			time.sleep(5)
			hb.check()
        	 
if __name__ == "__main__":

	daemon = ConvertDaemon('/tmp/convert-daemon.pid', '/dev/null', '/tmp/handleBarOut.log', '/tmp/handleBarError.log')
	
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