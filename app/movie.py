from lib import *
from app import *

class movie:
	
	def __init__(self, title):
		
		self.movieTitle = None
		self.movieImage = None
		self.movieName = None
		self.movieDescription = None
		self.movieRating = None
		self.movieReleased = None
		self.movieDirector = None
		self.movieProducer = None
		self.movieCast = None
		self.movieGenre = None
		self.imdbId = None
		self.foundMovie = False
		self.searchFailed = False
		
		self._setTitle(title)
		self._parseData()
					
	def _parseData(self):
		
		try:
			results = tmdb.search(self.getTitle())
			
			if not results:
				return False
			
			self.foundMovie = True
			
			movie = tmdb.getMovieInfo(results[0]['id'])
	
			self._setImage(movie['images'][0])
			self._setName(movie['name'])
			self._setDescription(movie['overview'])
			self._setRating(movie['rating'])
			self._setReleased(movie['released'])
			self._setDirector(movie['cast']['director'][0]['name'])
			self._setGenre(movie['categories']['genre'].keys()[0])
			self._setImdb(movie['imdb_id'])
			self._setProducer(movie['cast']['producer'][0]['name'])
			self._setCast(movie['cast']['actor'])
						
			return self
			
		except:
			print "Unexpected error:", sys.exc_info()[0]
			self.searchFailed = True
	
	def _setTitle(self, title):
		
		if title is not None:
			self.movieTitle = str(title).encode('utf-8').strip()
			
	def _setImage(self, image):
		
		if image is not None:
			self.movieImage = str(self._getImage(image)).encode('utf-8').strip()
			
	def _setName(self, name):
		
		if name is not None:
			self.movieName = str(name).encode('utf-8').strip()
			
	def _setDescription(self, description):
		
		if description is not None:
			self.movieDescription = str(description).encode('utf-8').strip()
			
	def _setRating(self, rating):
		
		if rating is not None:
			self.movieRating = str(rating).encode('utf-8').strip()
			
	def _setReleased(self, released):
		
		if released is not None:
			self.movieReleased = str(released).encode('utf-8').strip()
			
	def _setDirector(self, director):
		
		if director is not None:
			self.movieDirector = str(director).encode('utf-8').strip()
			
	def _setProducer(self, producer):
		
		if producer is not None:
			self.movieProducer = str(producer).encode('utf-8').strip()
			
	def _setGenre(self, genre):
		
		if genre is not None:
			self.movieGenre = str(genre).encode('utf-8').strip()
			
	def _setImdb(self, imdbId):
		
		if imdbId is not None:
			self.imdbId = str(imdbId).encode('utf-8').strip()
	
	def _setCast(self, cast):
		
		actors = []
		for actor in cast:
			
			actors.extend("," + actor['name'])
		
		self.movieCast = "".join(actors)[1:]
				
	def _getImage(self, images):
		
		for key in images.keys():
			
			if key == 'original':
				return images[key]
			elif key == 'cover':
				return images[key]
			else:
				pass
	
	def getTitle(self):				
		
		if self.movieTitle is not None:
			return self.movieTitle
		else:
			return "Unknown"
			
	def getImage(self):				
		
		if self.movieImage is not None:
			return self.movieImage
		else:
			return ""
			
	def getName(self):				
		
		if self.movieName is not None:
			return self.movieName
		else:
			return ""
			
	def getDescription(self):				
		
		if self.movieDescription is not None:
			return self.movieDescription
		else:
			return ""
			
	def getRating(self):				
		
		if self.movieRating is not None:
			return self.movieRating
		else:
			return ""
			
	def getReleased(self):				
		
		if self.movieReleased is not None:
			return self.movieReleased
		else:
			return ""
			
	def getDirector(self):				
		
		if self.movieDirector is not None:
			return self.movieDirector
		else:
			return ""
			
	def getProducer(self):				
		
		if self.movieProducer is not None:
			return self.movieProducer
		else:
			return ""
			
	def getCast(self):				
		
		if self.movieCast is not None:
			return self.movieCast
		else:
			return ""
			
	def getGenre(self):				
		
		if self.movieGenre is not None:
			return self.movieGenre
		else:
			return ""
			
	def getImdbId(self):				
		
		if self.imdbId is not None:
			return self.imdbId
		else:
			return ""
	
	