import functions as f
import random
import numpy as np
import matplotlib.pyplot as plt

def crawl(url, depth):
	'''
	Crawl the yt web graph and return relevance index 
	upto defined depth.
	'''
	if depth == 0:
		return 1
	
	tags, links = f.getDataFromUrl(url)
	if tags == None and links == None:
		print("---\tpage issues...skipping page")
		return -1
	relevance = []
	# Calculate Relevance with all links
	for link in links[:10]:
		temp_tags, _ = f.getDataFromUrl(link)
		if temp_tags == None:
			print("---\tpage issues...skipping page")
			continue
		relevance.append(f.getRelevance(tags, temp_tags))

	relevance_index_self = sum(relevance)/len(relevance)
	# Crawl only 3 random links
	relevance_child = []
	for link in random.sample(links,3):
		temp = crawl(link, depth-1)
		if temp!=-1:
			relevance_child.append(temp)

	avg_relevance_child = 0
	if len(relevance_child):
		avg_relevance_child = sum(relevance_child)/len(relevance_child)
	prob_rele_depth = relevance_index_self*avg_relevance_child
	return prob_rele_depth

def visualize_results(results):
	y = np.array([np.array(x) for x in results])
	y_avg = np.average(y, axis=1)
	for i in range(y.shape[0]):
		plt.plot(y[i], c='b', alpha=0.2)
	plt.plot(y_avg, c='r')

# Start URLs
urls = []
with open("links.txt","r") as file:
	urls = file.readlines()

# Each item in this list is a list with relevance 
# at different depths signified by their indices
results_for_urls = []
depth_range = 3
num_links = 5 # MAx31
lim_urls = urls[:num_links]
for index, url in enumerate(lim_urls):
	result = []
	for depth in range(depth_range):
		print("FOR \turl#{}/{} \twith depth={}/{}".format(index + 1, len(lim_urls), depth, depth_range))
		result.append(crawl(url, depth))
	results_for_urls.append(result)

visualize_results(results_for_urls)


