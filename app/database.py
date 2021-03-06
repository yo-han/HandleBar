import os, sys, datetime
import sqlite3 as lite

path = os.path.abspath(os.path.dirname(__file__)) + "/../"

""" App support path """
try:
	pf = file(path + "../configPath",'r')
	appSupportPath = pf.read().strip()
	pf.close()
except IOError:
	pass

if path.find("HandleBarApp.app") is not -1:
	dbPath = appSupportPath
else:
	dbPath = path

con = lite.connect(dbPath + '/handleBar.db')
con.text_factory = str

class Files(object):
	
	def new(self, type, name):
		
		with con:
			
			date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			
			cur = con.cursor()    
			cur.execute("INSERT INTO files (convertionDone, type, name, createDate) VALUES (0, ?, ?, ?)", (type, name, date))
			
			return cur.lastrowid
		
		return False
	
	def convertDone(self, fileId):
		
		uId = int(fileId)

		with con:
			cur = con.cursor() 
			cur.execute("UPDATE files SET convertionDone=1 WHERE fileId=:fileId", {"fileId":uId}) 
			
	def movie(self, fileId, title, image, artist, genre, releaseDate, description, rating, imdbId, hd):
		
		uId = int(fileId)
		
		if hd != "":
			uHD = 1
		else:
			uHD = 0
		
		with con:
			cur = con.cursor() 
			cur.execute("UPDATE files SET title=:title, image=:image, artist=:artist, genre=:genre, releaseDate=:releaseDate, description=:description, rating=:rating, imdbId=:imdbId, hd=:hd  WHERE fileId=:fileId", 
							{"fileId":uId, "image":image, "title":title, "artist":artist, "genre":genre, "releaseDate":releaseDate, "description":description, "rating":rating, "hd":uHD, "imdbId":imdbId}) 
		
	def episode(self, fileId, title, image, season, episode, network, episodeName, description, rating, airDate, genre, hd):

		uId = int(fileId)
		
		if hd != "":
			uHD = 1
		else:
			uHD = 0
		
		with con:
			cur = con.cursor() 
			cur.execute("UPDATE files SET title=:title, image=:image, season=:season, genre=:genre, releaseDate=:airDate, description=:description, rating=:rating, episode=:episode, episodeName=:episodeName, network=:network, hd=:hd  WHERE fileId=:fileId", 
							{"fileId":uId, "image":image, "title":title, "season":season, "genre":genre, "airDate":airDate, "description":description, "rating":rating, "hd":uHD, "episode":episode, "episodeName":episodeName, "network":network}) 
			
	def list(self):
		with con:    
		    
		    con.row_factory = lite.Row
		    
		    cur = con.cursor()    
		    cur.execute("SELECT * FROM files ORDER BY createDate DESC")
		
		    rows = cur.fetchall()
		
		    return rows
	
	def clearDb(self):
		with con:  
			cur = con.cursor()
			cur.execute("delete from files")
			cur.execute("delete from sqlite_sequence where name='files'")
