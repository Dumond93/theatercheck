#!/bin/python3


import requests
from bs4 import BeautifulSoup
import time
import subprocess

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

for i in getNowPlaying():
	print (i)
