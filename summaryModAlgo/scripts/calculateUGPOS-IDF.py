import sys
import re
import os
from nltk import word_tokenize, pos_tag


unigramsDF = {}

for f in os.listdir('../contextFiles/'):
	
	originalSents = []
	sents = []
	

	with open('../contextFiles/' + f) as inputFile:
		inputLines = [x.decode('utf-8',"replace").strip('\n').lower() for x in inputFile.readlines()]
		sentId = 0
		for line in inputLines:
			originalSents.append(line)
			#print line
			line = re.sub(r'\([^\)]*\)', '', line)
			line = re.sub(r'\[[^\]]*\]', '', line)
			line = re.sub(r'\s+', ' ', line)
			sents.append(line)
			sentId = sentId + 1

		documentTokens = []
		
		for line in sents:
			tokens = word_tokenize(line)
			tagTuples = pos_tag(tokens)
			print tagTuples
			tagsList = [t[1] for t in tagTuples]
			unigramsSet = list(tagsList)
			documentTokens.extend(unigramsSet)

		documentTokens = set(list(documentTokens))

		for token in documentTokens:
			if (token) not in unigramsDF:
				unigramsDF[token] = 1
			else:
				unigramsDF[token] = unigramsDF[token] + 1
				


with open('../IDFMetrics/UG-POS-IDF.txt', 'w') as output:
	for unigram in unigramsDF:
		output.write(unigram.encode('utf-8') + "\t" + str(unigramsDF[unigram]) + "\n")
			



