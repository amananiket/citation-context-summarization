import sys
import re
import os
from nltk import word_tokenize, pos_tag


for f in os.listdir('contextFiles/'):

	with open('preProcessOutput/' + f[:-4] + "-tempSents.txt") as inputFile:
		
		inputLines = {}

		for line in inputFile:
			inputLines[int(line.split("\t")[0])] = 	line.split("\t")[1].decode('utf-8',"replace").strip('\n').lower()
		
		outputFile = open('contextFiles-BG-POSTags/' + f, "w")

		
		for line in inputLines:
			tokens = word_tokenize(inputLines[line])
			tagTuples = pos_tag(tokens)
			tagsList = [t[1] for t in tagTuples]
			
			outputFile.write(str(line) + "\t" +  " ".join(tagsList) + "\n")


