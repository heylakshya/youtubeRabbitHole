import functions as f

url="https://www.youtube.com/watch?v=l5DLz7Ms11g"

tags, links = f.getDataFromUrl(url)
if tags == None and links == None:
	print("Internet issues...exiting")
	exit()

relevances = []
for link in links[:10]:
	tags_temp, _ = f.getDataFromUrl(link)
	if tags == None and links == None:
		print("Internet issues...skipping page")
		continue
	relevances.append(f.getRelevance(tags, tags_temp))

print(relevances, sum(relevances)/len(relevances))