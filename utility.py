import numpy as np
import json
embeddings_dict = {}
with open("glove.6B.50d.txt", 'r') as f:
	for i,line in enumerate(f):
		if(i%1000 == 0):
			print(i)
		values = line.split()
		word = values[0]
		vector = values[1:]
		embeddings_dict[word] = vector

# j = json.dumps(embeddings_dict)
# with open("embeddings.json","w") as f:
# 	f.write(j)
