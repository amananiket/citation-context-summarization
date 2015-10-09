import os
from difflib import SequenceMatcher


def getEdges():
	edgesList = []

	with open("../graphFeatures/edgesAAN.txt", "r") as inFile:
		for line in inFile:
			edgesList.append([line.split("\t")[0].strip(), line.split("\t")[1].strip()])

	return edgesList

def getInEdges(edgesList, paperID):

	return [x[0] for x in edgesList if x[1] == paperID]

def getOutEdges(edgesList, paperID):

	return [x[1] for x in edgesList if x[0] == paperID]

def findSimilarity(sent1, sent2):
	return SequenceMatcher(None, sent1, sent2).ratio()

def main():
	
	edgesList = getEdges()

	alreadyDoneList = []

	for f in os.listdir('../graphFeatures/inEdges/'):
		alreadyDoneList.append(f[:-4])

	for f in os.listdir("../contextFiles/"):
		if f[:-4] not in alreadyDoneList:

			inEdgesList = getInEdges(edgesList, f[:-4])

			inEdgesInfo = []

			for edge in inEdgesList:
				try :
					inputFile = open("../../../aan/papers_text/"+edge + ".txt")
					inputFileLines = []

					for iline in inputFile:
						inputFileLines.append(iline)

					inputFile.close()

					inEdgesInfo.append(inputFileLines)

				except:
					print "Error reading file ", edge

			contextFileLines = []

			inEdgesOutput = open("../graphFeatures/inEdges/"+ f, "w")

			contextFileInput = open("../contextFiles/"+f, "r")

			for line in contextFileInput:
				contextFileLines.append(line)

			contextFileInput.close()

			for line in contextFileLines:
				similarityList = []

				for edgeInfo in inEdgesInfo:
					maxSimilarity = max([findSimilarity(line, sent) for sent in edgeInfo])
					similarityList.append([inEdgesList[inEdgesInfo.index(edgeInfo)], maxSimilarity])

				similarities = [x[1] for x in similarityList]
				print similarityList
				inEdge = similarityList[similarities.index(max(similarities))][0]
				print inEdge, f
				inEdgesOutput.write(inEdge + "\n")

			inEdgesOutput.close()

if __name__ == "__main__":
	main()



