#!/usr/bin/python3
# Andre Dumond
# API Theater Script

import requests
from bs4 import BeautifulSoup
import time
import subprocess
from datetime import datetime
from plexapi.server import PlexServer
import sys

# Get the plex information for the plex server and login using token
baseurl = sys.argv[1]
token = sys.argv[2]
plex = PlexServer(baseurl, token)

# Get the plex movies library
MovieLibrary = plex.library.section(sys.argv[3]) # Get Movies Library

currentYear = datetime.now().year
previousYear = currentYear - 1

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[1;33m'
    ENDC = '\033[0m'

# Get the movies collection if it exists, if not create the collection
def getCollection(collectionVideos):
	MovieLibrary = plex.library.section(sys.argv[3])
	try:
		theaterCollection = MovieLibrary.collection('In Theaters')
	except:
		theaterCollection = MovieLibrary.createCollection('In Theaters', items=collectionVideos, smart=False, limit=None, libtype=None, sort=None, filters=None)
		hub = theaterCollection.visibility()
		hub.updateVisibility(recommended=True, home=True, shared=True)
		hub.reload()
		print ("Theater collection does not exist, creating collection...")
	return theaterCollection

# Get now playing in theaters movies from fandango
def getNowPlaying():
	print ("Getting now playing movies from https://www.fandango.com/movies-in-theaters")
	nowPlayingMovies = []
	URL = "https://www.fandango.com/movies-in-theaters"
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, "html.parser")

	elements = soup.find_all('span', class_='heading-style-1 browse-movielist--title poster-card--title')

	for element in elements:
		movieString = str(element.text)[:-7]
		nowPlayingMovies.append(movieString)
	return nowPlayingMovies

# search the plex server library for movies from the fandango movies in theaters page
def getMoviesFromPlex(nowPlaying):
	print ("Getting items from plex library for comparison")
	collectionVideos = []
	for i in nowPlaying:
		for video in MovieLibrary.search(i):
			if video.type == "movie":
				if video.title == i:
					print ("Theater move title " + i + " matches plex library title " + video.title + " with video year " + str(video.year))
					if video.year == currentYear or video.year == previousYear:
						collectionVideos.append(video)
	return collectionVideos

# Get movies that are already in the IN THEATERS collection
def getMoviesInCollection(theaterCollection):
	moviesInCollection = theaterCollection.items()
	return moviesInCollection

def addMoviesToCollection(theaterCollection, collectionVideos, moviesInCollection):
	finalAddedMovies= []
	for item in collectionVideos:
		if item in moviesInCollection:
			continue
		else:
			print (f"{Colors.GREEN}adding {Colors.ENDC}" + item.title)
			finalAddedMovies.append(item)

	if len(finalAddedMovies) != 0:
		theaterCollection.addItems(finalAddedMovies)
		print ("added " + str(len(finalAddedMovies)) + " items to collection")
	else:
		print (f"{Colors.YELLOW}No new items to add to the collection{Colors.ENDC}")

def removeMoviesFromCollection(theaterCollection, moviesInCollection, collectionVideos):
	finalRemovedMovies= []
	for item in moviesInCollection:
		if item in collectionVideos:
			continue
		else:
			finalRemovedMovies.append(item)

	if len(finalRemovedMovies) != 0:
		theaterCollection.removeItems(finalRemovedMovies)
	else:
		print(f"{Colors.YELLOW}There is nothing to remove from the collection{Colors.ENDC}") 
		

# Main
print ("Theater Checker running")
while True:
	nowPlaying = getNowPlaying()
	collectionVideos = getMoviesFromPlex(nowPlaying)
	theaterCollection = getCollection(collectionVideos)
	moviesInCollection = getMoviesInCollection(theaterCollection)
	addMoviesToCollection(theaterCollection, collectionVideos, moviesInCollection)
	removeMoviesFromCollection(theaterCollection, moviesInCollection, collectionVideos)
	print ("Waiting " +sys.argv[4]+ " seconds before checking again...")
	time.sleep(int(sys.argv[4]))
