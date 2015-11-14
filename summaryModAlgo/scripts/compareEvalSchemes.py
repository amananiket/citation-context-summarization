import os
import sys
import numpy as np 
import matplotlib.pyplot as plt
import numpy

deltaList = []
schemes = ['pyramid']
alg = ['baselineCLexRank', 'modCLexRank']

def createDeltaList():
	global deltaList

	for f in os.listdir("../contextFiles"):
		paperInfo = {}
		paperInfo['paper'] = f
		paperInfo['delta'] = {}

		deltaList.append(paperInfo)



def getSIMMetrixDelta():

	global deltaList, alg, schemes

	inFile = open("../../SIMetrix-v1/eval/mappings.txt.ieval.micro", "r")

	attributesRead = False
	attributes = []
	simMetrics = []

	for line in inFile:
		if not attributesRead:
			line = line.strip()
			attributes = line.split(" ")
			attributesRead = True

		else:
			simMetric = {}

			for i in range(0, len(line.split(" "))):
				if i < 2:
					simMetric[attributes[i]] = line.split(" ")[i]
				else:
					simMetric[attributes[i]] = float(line.split(" ")[i])

			simMetrics.append(simMetric)

	methods = attributes[4:-2]
	#print simMetrics
	for paper in deltaList:
		
		for method in methods:
			for metric in simMetrics:
				if metric['inputId'] == paper['paper'] and metric['sysId'] == alg[1]:
					paper['delta'][method] = metric[method]		

			for metric in simMetrics:
				if metric['inputId'] == paper['paper'] and metric['sysId'] == alg[0]:
					paper['delta'][method] -= metric[method]

	#print deltaList
	schemes.extend(methods)

def getPyramidDelta():

	global deltaList, alg

	modAlgoFile = open("../metrics/modAlgoMetrics.txt", "r")

	for line in modAlgoFile:
		paperName, pValue = line.split("\t")

		for paper in deltaList:
			if paper['paper'] == paperName:
				paper['delta']['pyramid'] = float(pValue)

	modAlgoFile.close()

	baselineFile = open("../metrics/baselineMetrics.txt", "r")

	for line in baselineFile:
		paperName, pValue = line.split("\t")

		for paper in deltaList:
			if paper['paper'] == paperName:
				paper['delta']['pyramid'] -= float(pValue)


	baselineFile.close()



def plotDelta():
	global deltaList, schemes

	N = len(deltaList)

	ind = np.arange(N)
	colors = ['b','g','r', 'c','m','y','k']

	width = 1/float(len(schemes)) - 0.05
	#print width
	print len(schemes)

	fig, ax = plt.subplots()
	rects = []

	rectIndex= 0

	for scheme in schemes:
		delScores = []

		for paper in deltaList:
			delScores.append(paper['delta'][scheme])

		#print delScores

		rect =ax.bar(ind + rectIndex*width, tuple(delScores), width, color = colors[schemes.index(scheme)])
		rectIndex += 1
		rects.append(rect)

	ax.set_ylabel(' Delta Scores')
	ax.set_title('Delta scores for 2 algorithms across evaluation schemes')
	ax.set_xticks(ind + (rectIndex-1)*width)
	paperNames = [paper['paper'] for paper in deltaList]
	ax.set_xticklabels(tuple(paperNames), rotation='vertical')

	ax.legend(tuple([rects[i][0] for i in range(0, len(rects))]), tuple([schemes[i] for i in range(0, len(schemes))]))

	plt.show()

def getCorrCoef():
	global deltaList, schemes
	corrMatrix = numpy.zeros((len(schemes), len(schemes)))

	for scheme1 in schemes:
		for scheme2 in schemes:
			scheme1Scores = []
			scheme2Scores = []


			for paper in deltaList:
				scheme1Scores.append(paper['delta'][scheme1])
				scheme2Scores.append(paper['delta'][scheme2])

			corrMatrix[schemes.index(scheme1), schemes.index(scheme2)] = numpy.corrcoef(scheme1Scores, scheme2Scores)[0,1]


	return corrMatrix

def getMaxIndex(l):

	maxV = -1
	ind = -1
	index = 0
	for i in l:
		if i > maxV and i != 1.0:

			maxV = i 
			ind = index

		index += 1

	return ind

def main():

	global deltaList, alg, schemes
	createDeltaList()
	getSIMMetrixDelta()
	getPyramidDelta()

	
	plotDelta()
	corrMatrix =  getCorrCoef()

	print "Highest correlation with pyramid evaluation is for : ", schemes[getMaxIndex(corrMatrix[schemes.index('pyramid'),:])]
	print "corr score : ", corrMatrix[schemes.index('pyramid'), getMaxIndex(corrMatrix[schemes.index('pyramid'),:])]

	print [(schemes[i], corrMatrix[schemes.index('pyramid'),i]) for i in range(0, len(schemes)) ] # if corrMatrix[schemes.index('pyramid'),i] > 0


if __name__ == '__main__':
	main()