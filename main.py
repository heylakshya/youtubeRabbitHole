import functions as f

url="https://www.youtube.com/watch?v=ukzFI9rgwfU"

tags, links = f.getDataFromUrl(url)

print(tags)
print(links)