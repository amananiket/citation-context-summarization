import sys
import re
import os


SDTupDF = {}

for f in os.listdir('../contextFiles/'):
	
	originalSents = []
	sents = []
	

	with open('../stanfordDependencies/' + f) as inputFile:
		
		sentId = 0
		for line in inputFile:
			if (len(line.split("\t")) == 2):
				sents.append(eval(line.split("\t")[1]))
			sentId = sentId + 1

		documentTokens = []
		
		for line in sents:
			
			documentTokens.extend(line)

		documentTokens = set(list(documentTokens))

		for token in documentTokens:
			if (token) not in SDTupDF:
				SDTupDF[token] = 1
			else:
				SDTupDF[token] += 1
				


with open('../IDFMetrics/StanfordDepTuples-IDF.txt', 'w') as output:
	for tup in SDTupDF:
		output.write(str(tup) + "\t" + str(SDTupDF[tup]) + "\n")
			

