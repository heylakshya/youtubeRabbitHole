import functions as f
import random
import numpy as np
import matplotlib.pyplot as plt
import json

def crawl2(url, depth, first_call = 0, home_tags = None):
	'''
	Crawl the yt web graph and return relevance index
	upto defined depth.
	'''
	print("---\tat depth = {}".format(depth))
	if depth == 0:
		return []
	
	tags = home_tags
	links = None
	attempt=5
	while (tags==None or links==None) and attempt>0:
		attempt -= 1
		tags, links = f.getDataFromUrl(url)
		if tags == None or links == None:
			print("---\t---\tpage issues...retrying")
			continue
	
	if attempt==0:
		print("---\t---\tran out of attempts")
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
    fig = plt.gcf()
    fig.set_size_inches(10, 7)
    plt.show()

# Start URLs
urls = []
with open("links.txt","r") as file:
	urls = file.readlines()

urls = list(set(urls))
# Each item in this list is a list with relevance
# at different depths signified by their indices
results_for_urls = []
depth_range = 16
num_links = len(urls)
lim_urls = random.sample(urls,num_links)

results_for_json = {}
for index, url in enumerate(lim_urls):
    print("FOR \turl#{}/{}".format(index + 1, len(lim_urls)))
    try:
        result = crawl2(url, depth_range, 1)
    except:
        continue
    if len(result)==depth_range:
        # Save result in json
        results_for_json[url] = result
        with open("results_appended_new.json","w") as file:
            file.write(json.dumps(results_for_json))
            # links_done.add(url)
        results_for_urls.append(result)

visualize_results(results_for_urls)


