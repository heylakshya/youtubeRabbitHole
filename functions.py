import requests
import time
import re
import json
import numpy as np
import spacy

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from config import *

nlp = spacy.load('en_core_web_lg')

def getDataFromUrl(url):
	'''
	Returns tags for the video, and list of recommended videos for the specified URL of a youtube webpage
	'''
	chrome_option = Options()
	chrome_option.add_argument("--headless")
	chrome_option.add_argument("--window-size=1920x1080")
	driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_option)
	driver.get(url)
	try:
		w = WebDriverWait(driver, 10)
		w.until(EC.presence_of_all_elements_located((By.TAG_NAME,"ytd-compact-video-renderer")))
		print("---\tpage loaded")
	except:
		return None, None
	src = driver.page_source
	soup = BeautifulSoup(src, 'html.parser')
	body = soup.find("body")
	
	tags = []
	print("---\tExtracting Tags")
	tag1 = 'window["ytInitialPlayerResponse"] = '
	tag2 = 'if (window.ytcsi)'
	p1 = src.find(tag1)
	p2 = p1 + src[p1:].find(tag2)
	jsontext = src[p1 + len(tag1):p2]
	jsontext = jsontext.strip()
	jsontext = jsontext[:-1]
	jsondata = json.loads(jsontext)
	try:
		tags = jsondata["videoDetails"]["keywords"]
	except:
		return None, None


	print("---\tExtracting Links")

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
	print("---\tGot Data")
	return tags, links

def getRelevance(tags_source, tags_link):
	'''
	Return percentage relevance for two lists of tags
	'''
	print("---\tCalculating relevance")
	set1 = []
	set2 = []
	for tag in tags_source:
		set1 = set1 + tag.split()
	for tag in tags_link:
		set2 = set2 + tag.split()
	
	set1 = " ".join(list(set(set1)))
	set2 = " ".join(list(set(set2)))

	sentence1 = nlp(set1)
	sentence2 = nlp(set2)

	sentence1 = nlp(" ".join([token.lemma_ for token in sentence1]))
	sentence2 = nlp(" ".join([token.lemma_ for token in sentence2]))

	sentence1 = nlp(" ".join(set([token.lemma_ for token in sentence1 if not token.is_oov])))
	sentence2 = nlp(" ".join(set([token.lemma_ for token in sentence2 if not token.is_oov])))

	print("---\tsource:",sentence1)
	print("---\tlink:",sentence2)

	similar = []
	for word1 in sentence1:
		max_sim = 0
		for word2 in sentence2:
			max_sim = max(word1.similarity(word2),max_sim)
		similar.append(max_sim)
	
	similar_arr = np.array(similar)
	similarity = np.linalg.norm(similar_arr)/len(similar)
	print("---\tsimilarity: ",similarity)
	return similarity