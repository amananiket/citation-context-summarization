import sys
import re
from nltk.stem.porter import *

stemmer = PorterStemmer()
limit = sys.argv[1]
fileName = sys.argv[2]
cutOff = 0.0

sents = []
originalSents = []
files = []
files.append(fileName)

for f in files:
	with open(f) as inputFile:
		inputLines = [x.decode('utf-8').strip('\n').lower() for x in inputFile.readlines()]
		sentId = 0
		for line in inputLines:
			originalSents.append(line)
			#print line
			line = re.sub(r'\([^\)]*\)', '', line)
			line = re.sub(r'\[[^\]]*\]', '', line)
			line = re.sub(r'\s+', ' ', line)
			stemmedWords = [stemmer.stem(x) for x in line.split()]
			line = " ".join(stemmedWords)
			print line
			sents.append(line)
			sentId = sentId + 1


		if (sentId <= 3):
			summary = ""
			for i in range(0, sentId):
				summary += originalSents[i]

			#summaryOutput = open(f+"-C-LR.txt", "w")
			#summaryOutput.write(summary)
			#summaryOutput.close()
			exit()

		
			



