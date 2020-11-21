import requests
from bs4 import BeautifulSoup

def extract_tags(url):
	result = requests.get(url)
	src = result.content