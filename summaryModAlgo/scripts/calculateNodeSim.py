import math
import re
import sys
from nltk import word_tokenize, pos_tag
from nltk.util import bigrams
from nltk.corpus import stopwords

from getGraphEdges import getInEdges, getOutEdges, getEdges

def getIDFs(filename):
	with open("../IDFMetrics/"+filename,"r") as idfFile:
		idf = {}
		N = 0

		for line in idfFile:
			line = line.rstrip().split('\t')
			tok = line[0]
			idf[tok] = int(line[1])
			N = N + idf[tok]

		for token in idf:
			idf[token] = math.log(N/(1+float(idf[token])))

		return idf

idfDict = getIDFs("idf.txt")
bgIdfDict = getIDFs("BgIdf.txt")
UG_POS_idfDict = getIDFs("UG-POS-IDF.txt")
BG_POS_idfDict = getIDFs("BG-POS-IDF.txt")


def getLexSim(featureIndex, sent1, sent2):

	############## Unigrams TF-IDF vectorization ############3
	
	c1 = 0
	c2 = 0
	idf = 0
	c = 0
	rs1 = 0
	rs2 = 0
	
	if (featureIndex == 1):

		count1 = {}
		count2 = {}

		wordSet1 = re.split("\W+", sent1)
		wordSet1 = [w for w in wordSet1 if not w in stopwords.words('english')]
		
		for word in wordSet1:
			if word in count1:
				count1[word] = count1[word] + 1
			else:
				count1[word] = 1

		wordSet2 = re.split("\W+", sent2)
		wordSet2 = [w for w in wordSet2 if not w in stopwords.words('english')]

		for word in wordSet2:
			if word in count2:
				count2[word] = count2[word] + 1
			else:
				count2[word] = 1
		
		
		wordsList = list(set(wordSet1 + wordSet2))
		wordsList.sort()
		

		

		countC = {}

		for word in wordsList:
			if word in count1:
				c1 = count1[word]
			else:
				c1 = 0

			if word in count2:
				c2 = count2[word]
			else:
				c2 = 0


			if word in idfDict:
				idf = idfDict[word]
			else:	
				idf = 1
			c1 = c1 * idf
			c2 = c2 * idf
		
			c = c + c1*c2

			countC[word] = c1*c2
			
			rs1 = rs1 + c1*c1
			rs2 = rs2 + c2*c2

#	keys = sorted(countC, key = lambda token : countC[token], reverse = True)

#	for key in keys:
	
	elif (featureIndex == 2):
	################# Bigrams TF-IDF ######################3

		bigramsCount1 = {}
		bigramsCount2 = {}


		tokens1 = word_tokenize(sent1)
		bigramsSet1 = list(bigrams(tokens1))
		
		for bigram in bigramsSet1:
			if (bigram[0]+bigram[1]) in bigramsCount1:
				bigramsCount1[bigram[0]+bigram[1]] = bigramsCount1[bigram[0]+bigram[1]] + 1
			else:
				bigramsCount1[bigram[0]+bigram[1]] = 1


		tokens2 = word_tokenize(sent2)
		bigramsSet2 = list(bigrams(tokens2))
		
		for bigram in bigramsSet2:
			if (bigram[0]+bigram[1]) in bigramsCount2:
				bigramsCount2[bigram[0]+bigram[1]] = bigramsCount2[bigram[0]+bigram[1]] + 1
			else:
				bigramsCount2[bigram[0]+bigram[1]] = 1
		
		bigramsList = list(set(bigramsSet1 + bigramsSet2))
		bigramsList.sort()
		bigramsCountC = {}

		for bigram in bigramsList:
			if (bigram[0]+bigram[1]) in bigramsCount1:
				c1 = bigramsCount1[(bigram[0]+bigram[1])]
			else:
				c1 = 0

			if (bigram[0]+bigram[1]) in bigramsCount2:
				c2 = bigramsCount2[(bigram[0]+bigram[1])]
			else:
				c2 = 0


			if (bigram[0] + " " + bigram[1]) in bgIdfDict:
				idf = bgIdfDict[bigram[0] + " " + bigram[1]]
			else:	
				idf = 1

			c1 = c1 * idf
			c2 = c2 * idf
		
			c = c + c1*c2

			bigramsCountC[bigram[0]+bigram[1]] = c1*c2
			
			rs1 = rs1 + c1*c1
			rs2 = rs2 + c2*c2

		
	############## Unigram POS tags TF-IDF vectorization ############3
	
	elif (featureIndex == 4):

		tagCount1 = {}
		tagCount2 = {}

		#wordSet1 = re.split("\W+", sent1)
		wordTags1 = sent1.split()
		
		for word in wordTags1:
			if word in tagCount1:
				tagCount1[word] = tagCount1[word] + 1
			else:
				tagCount1[word] = 1

		
		#wordSet2 = re.split("\W+", sent2)
		wordTags2 = sent2.split()
		
		for word in wordTags2:
			if word in tagCount2:
				tagCount2[word] = tagCount2[word] + 1
			else:
				tagCount2[word] = 1

		tagsList = list(set(wordTags1 + wordTags2))
		tagsList.sort()
		

		

		countC = {}

		for word in tagsList:
			if word in tagCount1:
				c1 = tagCount1[word]
			else:
				c1 = 0

			if word in tagCount2:
				c2 = tagCount2[word]
			else:
				c2 = 0


			if word in UG_POS_idfDict:
				idf = UG_POS_idfDict[word]
			else:	
				idf = 1
			c1 = c1 * idf
			c2 = c2 * idf
		
			c = c + c1*c2

			countC[word] = c1*c2
			
			rs1 = rs1 + c1*c1
			rs2 = rs2 + c2*c2

#	keys = sorted(countC, key = lambda token : countC[token], reverse = True)

#	for key in keys:
	
	elif (featureIndex == 5):
	################# Bigram POS tags TF-IDF ######################3

		bigramsCount1 = {}
		bigramsCount2 = {}


		tokenTags1 = sent1.split()
		bigramsSet1 = list(bigrams(tokenTags1))
		
		for bigram in bigramsSet1:
			if (bigram[0]+bigram[1]) in bigramsCount1:
				bigramsCount1[bigram[0]+bigram[1]] = bigramsCount1[bigram[0]+bigram[1]] + 1
			else:
				bigramsCount1[bigram[0]+bigram[1]] = 1

		tokenTags2 = sent2.split()
		bigramsSet2 = list(bigrams(tokenTags2))
		
		for bigram in bigramsSet2:
			if (bigram[0]+bigram[1]) in bigramsCount2:
				bigramsCount2[bigram[0]+bigram[1]] = bigramsCount2[bigram[0]+bigram[1]] + 1
			else:
				bigramsCount2[bigram[0]+bigram[1]] = 1
		
		bigramsList = list(set(bigramsSet1 + bigramsSet2))
		bigramsList.sort()
		bigramsCountC = {}

		for bigram in bigramsList:
			if (bigram[0]+bigram[1]) in bigramsCount1:
				c1 = bigramsCount1[(bigram[0]+bigram[1])]
			else:
				c1 = 0

			if (bigram[0]+bigram[1]) in bigramsCount2:
				c2 = bigramsCount2[(bigram[0]+bigram[1])]
			else:
				c2 = 0


			if (bigram[0] + " " + bigram[1]) in BG_POS_idfDict:
				idf = BG_POS_idfDict[bigram[0] + " " + bigram[1]]
			else:	
				idf = 1

			c1 = c1 * idf
			c2 = c2 * idf
		
			c = c + c1*c2

			bigramsCountC[bigram[0]+bigram[1]] = c1*c2
			
			rs1 = rs1 + c1*c1
			rs2 = rs2 + c2*c2

		

	r = math.sqrt( rs1 * rs2)
		
	if (r == 0):
		value =  0
	else:
		value =  c/r

	return value


def getCitationCountSim(sent1Index, sent2Index, citationsCount):
	if sent1Index in citationsCount:
		c1 = citationsCount[sent1Index]
	else:
		c1 = 0

	if sent2Index in citationsCount:
		c2 = citationsCount[sent2Index]
	else:
		c2 = 0

	c = min(c1, c2)
	r = max(c1, c2)

	if (r == 0):
		return 0
	else:
		return c/float(r)


def getNodeSim(featureIndex, paper1ID, paper2ID, dataList):

############ Graph based similarity features ###################

	if (featureIndex == 6):
		## Bibilographic coupling

		p1OutEdgesList = getOutEdges(dataList, paper1ID)
		p2OutEdgesList = getOutEdges(dataList, paper2ID)
		commonList = set(p1OutEdgesList) & set(p2OutEdgesList)
		return len(commonList)/ float(min(len(p1OutEdgesList), len(p2OutEdgesList)))

	elif (featureIndex == 7):

		## Cocitation matrix

		p1InEdgesList = getInEdges(dataList, paper1ID)
		p2InEdgesList = getInEdges(dataList, paper2ID)

		if (len(p1InEdgesList) == 0 or len(p2InEdgesList) == 0):
			return 0
		else:
			commonList = set(p1InEdgesList) & set(p2InEdgesList)
			return len(commonList)/ float(min(len(p1InEdgesList), len(p2InEdgesList)))


	elif (featureIndex == 8):

		## Title similarity
		if (paper1ID not in dataList or paper2ID not in dataList):
			return 0

		title1 = dataList[paper1ID]
		title2 = dataList[paper2ID]


		return getLexSim(1, title1, title2)

	elif (featureIndex == 9):

		## Author similarity
		if (paper1ID not in dataList or paper2ID not in dataList):
			return 0

		authorList1 = dataList[paper1ID]
		authorList2 = dataList[paper2ID]

		commonAuthorSet = set(authorList1) & set(authorList2)

		return len(commonAuthorSet)/float(min(len(authorList1), len(authorList2)))

	elif (featureIndex == 10):

		## time similarity

		year1 = dataList[paper1ID]
		year2 = dataList[paper2ID]

		return max(0, (1- (float(abs(int(year1) - int(year2)))/5)))

def main():
	optionIndex = int(sys.argv[2])
	sims = open("../preProcessOutput/"+sys.argv[1]+"-modSimMetrics.txt", "w")

	
	if (optionIndex == 0):
		featureMetrics = {}
		for i in range(1,11):
			featureMetrics[i] = calculateFeatureNodeSim(i)
		
		featureWeights = {}
		weightsInputFile = open("../metrics/featureWeightsHeuristic1.txt", "r")

		for line in weightsInputFile:
			values = line.split()
			featureWeights[int(values[0])] = float(values[1])

		numberOfSentences = len(featureMetrics[1])
		
		similarityMetrics = []

		for i in range(0, numberOfSentences):
			tempList = [0]*numberOfSentences
			similarityMetrics.append(tempList)

		for i in range(0, numberOfSentences):
			for j in range(0, numberOfSentences):

				for k in range(1,11):
					similarityMetrics[i][j] += featureWeights[k]*featureMetrics[k][i][j]


	elif (optionIndex == 11):
		#### Combining features with top 2 scores ######

		featureMetrics = {}
		##for i in range(1,11):
		featureMetrics[0] = calculateFeatureNodeSim(1)
		featureMetrics[1] = calculateFeatureNodeSim(4)
		
		# featureWeights = {}
		# weightsInputFile = open("../metrics/featureWeightsHeuristic1.txt", "r")

		# for line in weightsInputFile:
		# 	values = line.split()
		# 	featureWeights[int(values[0])] = float(values[1])

		numberOfSentences = len(featureMetrics[1])
		
		similarityMetrics = []

		for i in range(0, numberOfSentences):
			tempList = [0]*numberOfSentences
			similarityMetrics.append(tempList)

		for i in range(0, numberOfSentences):
			for j in range(0, numberOfSentences):

				# for k in range(1,11):
				similarityMetrics[i][j] += (featureMetrics[0][i][j] + featureMetrics[1][i][j])/2


	else:
		similarityMetrics = calculateFeatureNodeSim(optionIndex)
		numberOfSentences = len(similarityMetrics)

	for i in range(0, numberOfSentences):
		for j in range(0, numberOfSentences):
			sims.write(str(i+1) + "\t" + str(j+1) + "\t" + str(similarityMetrics[i][j]) + "\n")


def calculateFeatureNodeSim(featureIndex):

	

	if (featureIndex in [1,2]):
		inputFile =  open("../preProcessOutput/"+sys.argv[1]+"-tempSents.txt")

		inputLines = {}

		for line in inputFile:
			inputLines[int(line.split("\t")[0])] = 	line.split("\t")[1].decode('utf-8',"replace").strip('\n').lower()

	elif (featureIndex == 3):
		citationsCount = {}

		with open("../contextFiles/" + sys.argv[1] + ".txt", "r") as context:
			lineId = 0
			for line in context:
				tokens = [x.decode('utf-8',"replace") for x in re.split("\W+", line)]
				for token in tokens:
					try:
						int(token)
						if (len(token) == 4):
							if lineId in citationsCount:
								citationsCount[lineId] = citationsCount[lineId] + 1
							else:
								citationsCount[lineId] = 1
					except:
						continue

				lineId = lineId + 1

		featureMetrics = []

		for i in range(0, lineId):
			tempList = [0]*lineId
			featureMetrics.append(tempList)

		for i in range(0, lineId):
			for j in range(0, lineId):
				featureMetrics[i][j] = getCitationCountSim(i, j, citationsCount)

	elif (featureIndex == 4):
		inputFile =  open("../contextFiles-UG-POSTags/"+sys.argv[1]+".txt")

		inputLines = {}

		for line in inputFile:
			inputLines[int(line.split("\t")[0])] = 	line.split("\t")[1]

	elif (featureIndex == 5):
		inputFile =  open("../contextFiles-BG-POSTags/"+sys.argv[1]+".txt")

		inputLines = {}

		for line in inputFile:
			inputLines[int(line.split("\t")[0])] = 	line.split("\t")[1]

	#inputLines = [x.decode('utf-8').strip('\n').lower() for x in inputFile.readlines()]
	#sentId = 0
	

	if (featureIndex in [1,2,4,5]):

		featureMetrics = []

		for i in range(0, len(inputLines)):
			tempList = [0]*len(inputLines)
			featureMetrics.append(tempList)

		for i in range(0, len(inputLines)):
			for j in range(0, len(inputLines)):
				featureMetrics[i][j] = getLexSim(featureIndex, inputLines[i+1] , inputLines[j+1])

	# if (featureIndex in [1,2,4,5]):
	# 	for sent1 in inputLines:
	# 		for sent2 in inputLines:
	# 			sims.write(str(sent1) + "\t" + str(sent2) + "\t" + str() + "\n")



	if (featureIndex in [6, 7, 8, 9, 10]):

		if featureIndex in [6,7]:
			dataList = getEdges()

		elif (featureIndex == 8):
			inputFile = open("../graphFeatures/titles.txt")
			dataList = {}

			for line in inputFile:
				titlePair = line.decode("utf-8", "replace").split("\t")
				dataList[titlePair[0]] = titlePair[1]

		elif (featureIndex == 9):
			inputFile = open("../graphFeatures/authors.txt")	
			dataList = {}

			for line in inputFile:
				authorsData = line.decode("utf-8", "replace").split("\t")
				dataList[authorsData[0]] = [authorsData[x] for  x in range(1,len(authorsData))]

		elif (featureIndex == 10):

			inputFile = open("../graphFeatures/years.txt")	
			dataList = {}

			for line in inputFile:
				yearData = line.decode("utf-8", "replace").split("\t")
				dataList[yearData[0]] = int(yearData[1])


		inputFile = open("../graphFeatures/inEdges/"+sys.argv[1] + ".txt", "r")
		filePapersList = []
		lines = 0

		for line in inputFile:
			lines += 1
			filePapersList.append(line.strip())


		featureMetrics = []

		for i in range(0, lines):
			tempList = [0]*lines
			featureMetrics.append(tempList)
	
		for i in range(0, lines):
			for j in range(0, lines):
				featureMetrics[i][j] = getNodeSim(featureIndex, filePapersList[i], filePapersList[j], dataList)


		# for i in range(1, lines+1):
		# 	for j in range(1, lines+1):
		# 		sims.write(str(i) + "\t" + str(j) + "\t" + str(getNodeSim(featureIndex, filePapersList[i-1], filePapersList[j-1], dataList)) + "\n")				


	return featureMetrics


if __name__ == "__main__":
	main()