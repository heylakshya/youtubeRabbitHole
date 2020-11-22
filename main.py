import functions as f
import random
import numpy as np
import matplotlib.pyplot as plt

def crawl2(url, depth, first_call = 0, home_tags = None):
	'''
	Crawl the yt web graph and return relevance index
	upto defined depth.
	'''
	print("---\tat depth = {}".format(depth))
	if depth == 0:
		return []

	tags, links = f.getDataFromUrl(url)
	if tags == None and links == None:
		print("---\t---\tpage issues...returning empty")
		return []

	temp_tags = None
	attempt = 10
	while temp_tags==None and attempt>0:
		attempt -= 1
		link = random.choice(links)
		temp_tags, _ = f.getDataFromUrl(link)
		if temp_tags == None:
			print("---\t---\tpage issues...skipping page")
			continue
	if attempt==0:
		print("---\t---\tran out of attempts")
		return []
	relevance_list = []
	relevance = 0
	if first_call==0:
		tags = home_tags
	relevance = f.getRelevance(tags, temp_tags)
	relevance_list.append(relevance)
	return_list = crawl2(link, depth-1, 0, tags)
	# scaled_return_list = []
	# for item in return_list:
		# scaled_return_list.append(item*relevance)
	relevance_list = relevance_list + return_list
	return relevance_list

def visualize_results(results):
	y = np.array([np.array(x) for x in results])
	y_avg = np.average(y, axis=0)
	for i in range(y.shape[0]):
		plt.plot(y[i], marker='o', color='b', alpha=0.2)
	plt.plot(y_avg, marker='o', color='r')
	plt.xlabel("Depth of rabbit hole")
	plt.ylabel("Relevance to root video")
	plt.show()

# Start URLs
urls = []
with open("links.txt","r") as file:
	urls = file.readlines()

# Each item in this list is a list with relevance
# at different depths signified by their indices
results_for_urls = []
depth_range = 8
num_links = 12 # MAx31
lim_urls = random.sample(urls,num_links)
for index, url in enumerate(lim_urls):
	print("FOR \turl#{}/{}".format(index + 1, len(lim_urls)))
	result = crawl2(url, depth_range, 1)
	if len(result)==depth_range:
		results_for_urls.append(result)

visualize_results(results_for_urls)


