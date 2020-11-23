import requests
import time
import re
import json
import numpy as np
import spacy
import random
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

nlp = spacy.load('en_core_web_lg')

def getDataFromUrl(url):
    '''
    Returns tags for the video, and list of recommended videos for the specified URL of a youtube webpage
    '''
    driver = webdriver.Chrome('chromedriver',options=chrome_options)
    driver.get(url)

    try:
        w = WebDriverWait(driver, 1000)
        w.until(EC.presence_of_all_elements_located((By.TAG_NAME,"ytd-compact-video-renderer")))
        print("---\tpage loaded")
    except:
        return None, None
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    body = soup.find("body")

    tags = []
    # print("---\tExtracting Tags")
    tag1 = 'window["ytInitialPlayerResponse"] = '
    tag2 = 'if (window.ytcsi)'
    p1 = src.find(tag1)
    p2 = p1 + src[p1:].find(tag2)
    jsontext = src[p1 + len(tag1):p2]
    jsontext = jsontext.strip()
    jsontext = jsontext[:-1]
    try:
        jsondata = json.loads(jsontext)
        tags = jsondata["videoDetails"]["keywords"]
    except:
        return None, None


    # print("---\tExtracting Links")

    items = body.find_all("ytd-compact-video-renderer")

    links = []

    for item in items:
        temp = item.find("div", id="dismissable")
        temp = temp.find("ytd-thumbnail")
        link = temp.find("a", id="thumbnail", href=True)
        links.append('https://www.youtube.com' + link['href'])
    driver.close()
    # print("---\tGot Data")
    return tags, links

def getRelevance(tags_source, tags_link):
    '''
    Return percentage relevance for two lists of tags
    '''
    # print("---\tCalculating relevance")
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

    sentence1 = nlp(" ".join(set([token.lemma_ for token in sentence1 if token.lemma_ in nlp.vocab]) - stopwords))
    sentence2 = nlp(" ".join(set([token.lemma_ for token in sentence2 if token.lemma_ in nlp.vocab]) - stopwords))

    # print("---\tsource:",sentence1)
    # print("---\tlink:",sentence2)


    list1 = [token.vector for token in sentence1]
    list2 = [token.vector for token in sentence2]
    if len(list1)!=0 and len(list2)!=0:
        vec1 = sum(list1)/len(list1)
        vec2 = sum(list2)/len(list2)
    else:
        return float(0)

    print(vec1.shape)
    print(vec1)
    similarity = float(vec1.dot(vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
    print("---\tsimilarity: ",similarity)
    return similarity