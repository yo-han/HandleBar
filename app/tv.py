from lib import *
from app import *

class tvEpisode:
	
	def __init__(self, serieData):
		
		self.seriesTitle = None
		self.seriesSeason = None
		self.seriesEpisode = None
		self.seriesEpisodeName = None
		self.seriesDescription = None
		self.seriesRating = None
		self.seriesAirDate = None
		self.seriesNetwork = None
		self.seriesGenre = None
		self.seriesImage = None
		self.foundSeries = False
		
		self._setTitle(serieData['series'])
		
		if "season" in serieData:
						
			self._setSeason(serieData['season'])
			self._setEpisode(serieData['episodeNumber'])

		self._parseData()
							
	def _parseData(self):

		if self.seriesSeason is None:
			return False

		try:
			tvdb = tvdb_api.Tvdb(banners=True)
			
			title = self.getTitle()
			series = tvdb[title]
			season = int(self.getSeason())
			episode = int(self.getEpisode())
	
			self._setArtwork(series['_banners']['season']['season'], season, tvdb)
			self._setTitle(series['seriesname'])
			self._setEpisodeName(series[season][episode]['episodename'])
			self._setEpisodeDescription(series[season][episode]['overview'])
			self._setAirDate(series[season][episode]['firstaired'])
			self._setNetwork(series['network'])
			self._setGenre(series['genre'])
			self._setRating(series['contentrating'])		
			
			self.foundSeries = True
			
		except:
			print "Unexpected error:", sys.exc_info()[0]
			return False
			
	def _setTitle(self, title):
		
		if title is not None:
			self.seriesTitle = str(title).encode('utf-8').strip()
			
	def _setSeason(self, season):
		
		if season is not None:
			self.seriesSeason = str(season).encode('utf-8').strip()
	
	def _setEpisode(self, episode):
		
		if episode is not None:
			self.seriesEpisode = str(episode).encode('utf-8').strip()
			
	def _setEpisodeName(self, episodeName):
		
		if episodeName is not None:
			self.seriesEpisodeName = str(episodeName).encode('utf-8').strip()
			
	def _setEpisodeDescription(self, episodeDescription):
		
		if episodeDescription is not None:
			self.seriesDescription = episodeDescription.encode('utf-8').strip()
			
	def _setAirDate(self, airdate):
		
		if airdate is not None:
			self.seriesAirDate = str(airdate).encode('utf-8').strip()

	def _setNetwork(self, network):
		
		if network is not None:
			self.seriesNetwork = str(network).encode('utf-8').strip()
			
	def _setGenre(self, genre):
		
		if genre is not None:
			genre = (genre)[1:len(genre)]
			self.seriesGenre = genre[0:genre.find("|")].encode('utf-8').strip()
	
	def _setRating(self, rating):
		
		if rating is not None:
			self.seriesRating  = rating.encode('utf-8').strip()
	
	def _setArtwork(self, banners, season, tvdb):

		for s in banners:
			artwork = tvdb[self.getTitle()]['_banners']['season']['season'][s]
			
			if artwork['language'] == "en" and int(artwork['season']) == season:
				self.seriesImage = artwork['_bannerpath']
				break
				
	def getTitle(self): 
		if self.seriesTitle is not None:
			return self.seriesTitle
		else:
			return "Unknown"
			
	def getTitleClean(self):
	
		_title = self.getTitle()
		if _title.find('revolution.') != -1:
			title = _title[:-5]
		else:
			title = _title
			
		return title
		
			
	def getSeason(self): 
		if self.seriesSeason is not None:
			return self.seriesSeason
		else:
			return ""
			
	def getEpisode(self): 
		if self.seriesEpisode is not None:
			return self.seriesEpisode
		else:
			return ""
			
	def getEpisodeName(self): 
		if self.seriesEpisodeName is not None:
			return self.seriesEpisodeName
		else:
			return ""
	
	def getDescription(self): 
		if self.seriesDescription is not None:
			return self.seriesDescription
		else:
			return ""
			
	def getRating(self): 
		if self.seriesRating is not None:
			return self.seriesRating
		else:
			return ""
			
	def getGenre(self): 
		if self.seriesGenre is not None:
			return self.seriesGenre
		else:
			return ""
	
	def getImage(self): 
		if self.seriesImage is not None:
			return self.seriesImage
		else:
			return ""
			
	def getNetwork(self): 
		if self.seriesNetwork is not None:
			return self.seriesNetwork
		else:
			return ""
			
	def getAirdate(self): 
		if self.seriesAirDate is not None:
			return self.seriesAirDate
		else:
			return ""