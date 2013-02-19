#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
HandleBar
"""

import os
import sys
import glob
import time
from app import *
from lib import *

projectDir = HandleBarConfigPath

class metadata:

        """
        A generic daemon class.
       
        Usage: subclass the Daemon class and override the run() method
        """
        def __init__(self, file, fileId):
 
        	self.filePath = file
        	self.fileId = fileId
        	self.AtomicParsleyPath = HandleBarBinPath + "/bin/AtomicParsley"
        	self.SublerCLIPath = HandleBarBinPath + "/bin/SublerCLI"
        	self.subtitlePath = os.path.abspath(HandleBarConfigPath + "/" + SubtitlePath + "/" + os.path.basename(self.filePath)).replace('.m4v','.srt')
        	
        	self.guess = guessit.guess_video_info(self.filePath, info = ['filename'])
        	
        def addSubtitles(self, originalFilePath):
	        print self.subtitlePath
        	if os.path.exists(self.subtitlePath):
				arguments = [self.SublerCLIPath, "-dest", originalFilePath, "-source", self.subtitlePath,"-language",SubtitleLanguage]
				print originalFilePath	
				logProc = open("/tmp/SublrCLI.log", "a")
				subprocess.Popen(arguments, shell=False, stdout=logProc, stderr=subprocess.STDOUT, preexec_fn = self.preexec).communicate()
               	
        def parseFile(self):
	           	   		
        	return self.setMetaData(self.guess)
        
        def setMetaData(self, guess):
            
            if "screenSize" in guess and (guess['screenSize'] == '720p' or guess['screenSize'] == '1080p'):
            	hdb = "1"
            else:
            	hdb = "0"
            	
            if os.path.exists(self.subtitlePath):
            	subtitles = self.subtitlePath
            else:
            	subtitles = ""
   	          	               	
            if guess['type'] == "movie":
				
            	print "Movie"
					
            	mvd = movie(guess['title'])

            	if mvd.foundMovie == False:
            		Notify('No data found for this movie', 'HandleBar')
            		return False
					
            	image = self.downloadImage(mvd.getImage())     
					
            	Notify('Set metadata movie:\n' + mvd.getName(), 'HandleBar')

            	tags = ["{Artwork:" + image + "}", 
            			"{HD Video:" + hdb + "}", 
            			"{Name:" + mvd.getName() + "}", 
            			"{Director:" + mvd.getDirector() + "}", 
            			"{Producer:" + mvd.getProducer() + "}", 
            			"{Cast:" + mvd.getCast() + "}", 
            			"{Genre:" + mvd.getGenre() + "}", 
            			"{Release Date:" + mvd.getReleased() + "}", 
            			"{Description:" + mvd.getDescription() + "}", 
            			"{Long Description:" + mvd.getDescription() + "}", 
            			"{Rating:" + mvd.getRating() + "}", 
            			"{contentID:" + mvd.getImdbId() + "}",
            			"{Media Kind:Movie}",
            			"{Comments:Original filename " + os.path.basename(self.filePath) + "}"]   
            			        	      	
            	arguments = [self.SublerCLIPath, "-optimize", "-dest", self.filePath, "-source", subtitles, "-metadata", "".join(tags),"-language",SubtitleLanguage]
				
            	logProc = open("/tmp/SublrCLI.log", "a")
            	subprocess.Popen(arguments, shell=False, stdout=logProc, stderr=subprocess.STDOUT, preexec_fn = self.preexec).communicate()

            	filesTable.movie(self.fileId, mvd.getName(), os.path.basename(image), mvd.getDirector(), mvd.getGenre(), mvd.getReleased(), mvd.getDescription(), mvd.getRating(), mvd.getImdbId(), hdb)
				
            	return True      	
            	
            elif guess['type'] == "episode":
				
            	print "TV Show"
				
            	episode = tvEpisode(guess)

            	if episode.foundSeries == False:
            		Notify('No data found for this episode', 'HandleBar')
            		return False

            	title = episode.getTitleClean()
            	image = self.downloadImage(episode.getImage())    
           					
            	Notify('Set metadata tv show:\n' + title, 'HandleBar')

            	tags = ["{Artwork:" + image + "}", 
            			"{HD Video:" + hdb + "}", 
            			"{TV Show:" + title + "}", 
            			"{TV Episode #:" + episode.getEpisode() + "}", 
            			"{TV Season:" + episode.getSeason() + "}", 
            			"{TV Network:" + episode.getNetwork() + "}", 
            			"{Name:" + episode.getEpisodeName() + "}", 
            			"{Genre:" + episode.getGenre() + "}", 
            			"{Release Date:" + episode.getAirdate() + "}", 
            			"{Description:" + episode.getDescription() + "}", 
            			"{Long Description:" + episode.getDescription() + "}", 
            			"{Rating:" + episode.getRating() + "}",
            			"{Director:" + episode.getCast() + "}",
            			"{Media Kind:TV Show}",
            			"{Comments:Original filename " + os.path.basename(self.filePath) + "}"]   
            			        	      	
            	arguments = [self.SublerCLIPath, "-optimize", "-dest", self.filePath, "-source", subtitles, "-metadata", "".join(tags),"-language",SubtitleLanguage]
				
            	logProc = open("/tmp/SublrCLI.log", "a")
            	subprocess.Popen(arguments, shell=False, stdout=logProc, stderr=subprocess.STDOUT, preexec_fn = self.preexec).communicate()
				
            	filesTable.episode(self.fileId, title, os.path.basename(image), episode.getSeason(), episode.getEpisode(), episode.getNetwork(), episode.getEpisodeName(), episode.getDescription(), episode.getRating(), episode.getAirdate(), episode.getGenre(), hdb)
				
            	return True
            else:
            	print "Unknown type"
            	return False										
			
        def preexec(self):
	    	os.setpgrp()
	    		
        def downloadImage(self, url):
        	
        	path = HandleBarConfigPath + '/media/images/' + os.path.basename(url)
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