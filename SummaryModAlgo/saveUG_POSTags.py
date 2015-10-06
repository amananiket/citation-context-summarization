import sys
import re
import os
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords


for f in os.listdir('contextFiles/'):

	with open('preProcessOutput/' + f[:-4] + "-tempSents.txt") as inputFile:
		
		inputLines = {}

		for line in inputFile:
			inputLines[int(line.split("\t")[0])] = 	line.split("\t")[1].decode('utf-8',"replace").strip('\n').lower()
		
		outputFile = open('contextFiles-UG-POSTags/' + f, "w")

		
		for line in inputLines:
			tokens = word_tokenize(inputLines[line])
			unigramTokens = [w for w in tokens if not w in stopwords.words('english')]
			tagTuples = pos_tag(unigramTokens)
			tagsList = [t[1] for t in tagTuples]
			
			outputFile.write(str(line) + "\t" +  " ".join(tagsList) + "\n")


