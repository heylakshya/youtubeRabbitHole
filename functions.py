import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import json

def getDataFromUrl(url):
	driver = webdriver.Chrome("./chromedriver")
	driver.get(url)
	time.sleep(5)

	src = driver.page_source
	soup = BeautifulSoup(src, 'html.parser')
	body = soup.find("body")
	
	tags = []

	tag1 = 'window["ytInitialPlayerResponse"] = '
	tag2 = 'if (window.ytcsi)'
	p1 = src.find(tag1)
	p2 = p1 + src[p1:].find(tag2)
	jsontext = src[p1 + len(tag1):p2]
	jsontext = jsontext.strip()
	jsontext = jsontext[:-1]
	jsondata = json.loads(jsontext)
	tags = jsondata["videoDetails"]["keywords"]

	items = body.find("ytd-app")
	items = items.find("div", id="content")
	items = items.find("ytd-page-manager", id="page-manager")
	items = items.find("ytd-watch-flexy")
	items = items.find("div", id="columns")
	items = items.find("div", id="secondary")
	items = items.find("div", id="secondary-inner")
	items = items.find("div", id="related")
	items = items.find("ytd-watch-next-secondary-results-renderer")
	items = items.find("div", id="items")
	items = items.find_all("ytd-compact-video-renderer")

	links = []

	for item in items:
		temp = item.find("div", id="dismissable")
		temp = temp.find("ytd-thumbnail")
		link = temp.find("a", id="thumbnail", href=True)
		links.append('https://www.youtube.com' + link['href'])
	driver.close()

	return tags, links