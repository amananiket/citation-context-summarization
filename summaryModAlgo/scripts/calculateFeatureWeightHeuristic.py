
featurePScores = [0.6658455015, 0.6212465025, 0.5800021814, 
				  0.6512963561, 0.5258799947, 0.5758991342,
				  0.4668755464, 0.5743987379, 0.5476835667,
				  0.5583852299]

def calculateHeuristic1():
	
	inputFile = open("../metrics/paperWiseScores.txt", "r")

	maxFeatureIndexes = {}

	for line in inputFile:
		scores = line.split()

		if len(scores) != 11:
			continue


		maxScore = max([float(scores[x]) for x in range(1,len(scores))])
		for i in range(1,len(scores)):
			if float(scores[i]) == maxScore:
				if scores[0] in maxFeatureIndexes:
					maxFeatureIndexes[scores[0]].append(i)
				else:
					maxFeatureIndexes[scores[0]] = [i]

	print maxFeatureIndexes

	featureWeightsDict = {}

	for paper in maxFeatureIndexes:
		for index in maxFeatureIndexes[paper]:
			if index in featureWeightsDict:
				featureWeightsDict[index] += 1/float(len(maxFeatureIndexes[paper]))
			else:
				featureWeightsDict[index] = 1/float(len(maxFeatureIndexes[paper]))

	out = open("../metrics/featureWeightsHeuristic1.txt", "w")

	for feature in featureWeightsDict:
		featureWeightsDict[feature]	= featureWeightsDict[feature]/float(len(maxFeatureIndexes))
		out.write(str(feature) + "\t" + str(featureWeightsDict[feature]) + "\n")

	out.close()


def calculateHeuristic3():
	
	inputFile = open("../metrics/paperWiseScores.txt", "r")

	maxFeatureIndexes = {}

	paperScores = []
	featuresList = []

	for line in inputFile:
		scores = line.split()

		if len(scores) != 11:
			continue
		paperScores.append(scores)

		for i in range(1, 11):
			if max([float(scores[x]) for x in range(1,11)]) == float(scores[i]):
				if float(scores[i]) > 0.95 and (max([float(scores[x]) for x in range(1,11)]) - min([float(scores[x]) for x in range(1,11)])) > 0.6:
					if i not in featuresList:
						featuresList.append(i)

	featuresList = sorted(featuresList)
	print featuresList
	for scores in paperScores:

		maxScore = max([float(scores[x]) for x in featuresList])
		for i in featuresList:
			if float(scores[i]) == maxScore:
				if scores[0] in maxFeatureIndexes:
					maxFeatureIndexes[scores[0]].append(i)
				else:
					maxFeatureIndexes[scores[0]] = [i]

	print maxFeatureIndexes

	featureWeightsDict = {}

	for paper in maxFeatureIndexes:
		for index in maxFeatureIndexes[paper]:
			if index in featureWeightsDict:
				featureWeightsDict[index] += 1/float(len(maxFeatureIndexes[paper]))
			else:
				featureWeightsDict[index] = 1/float(len(maxFeatureIndexes[paper]))

	out = open("../metrics/featureWeightsHeuristic4.txt", "w")

	for feature in featureWeightsDict:
		featureWeightsDict[feature]	= featureWeightsDict[feature]/float(len(maxFeatureIndexes))
		out.write(str(feature) + "\t" + str(featureWeightsDict[feature]) + "\n")

	out.close()


def calculateHeuristic5():
	
	inputFile = open("../metrics/paperWiseScores.txt", "r")

	maxFeatureIndexes = {}

	paperScores = []
	featuresList = []

	for line in inputFile:
		scores = line.split()

		if len(scores) != 11:
			continue
		paperScores.append(scores)

		for i in range(1, 11):
			if max([float(scores[x]) for x in range(1,11)]) == float(scores[i]):
				if (max([float(scores[x]) for x in range(1,11)]) - min([float(scores[x]) for x in range(1,11)])) > 0.6:
					if i not in featuresList:
						featuresList.append(i)

	featuresList = sorted(featuresList)
	print featuresList
	for scores in paperScores:

		maxScore = max([float(scores[x]) for x in featuresList])
		for i in featuresList:
			if float(scores[i]) == maxScore:
				if scores[0] in maxFeatureIndexes:
					maxFeatureIndexes[scores[0]].append(i)
				else:
					maxFeatureIndexes[scores[0]] = [i]

	print maxFeatureIndexes

	featureWeightsDict = {}

	for paper in maxFeatureIndexes:
		for index in maxFeatureIndexes[paper]:
			if index in featureWeightsDict:
				featureWeightsDict[index] += 1/float(len(maxFeatureIndexes[paper]))
			else:
				featureWeightsDict[index] = 1/float(len(maxFeatureIndexes[paper]))

	out = open("../metrics/featureWeightsHeuristic4.txt", "w")

	for feature in featureWeightsDict:
		featureWeightsDict[feature]	= featureWeightsDict[feature]/float(len(maxFeatureIndexes))
		out.write(str(feature) + "\t" + str(featureWeightsDict[feature]) + "\n")

	out.close()

	
def calculateHeuristic2():

	inputFile = open("../metrics/paperWiseScores.txt", "r")

	maxFeatureIndexes = {}

	for line in inputFile:
		scores = line.split()

		if len(scores) != 11:
			continue


		maxScore = max([float(scores[x]) for x in [1,2,4]])
		for i in [1,2,4]:
			if float(scores[i]) == maxScore:
				if scores[0] in maxFeatureIndexes:
					maxFeatureIndexes[scores[0]].append(i)
				else:
					maxFeatureIndexes[scores[0]] = [i]

	print maxFeatureIndexes

	featureWeightsDict = {}

	for paper in maxFeatureIndexes:
		for index in maxFeatureIndexes[paper]:
			if index in featureWeightsDict:
				featureWeightsDict[index] += 1/float(len(maxFeatureIndexes[paper]))
			else:
				featureWeightsDict[index] = 1/float(len(maxFeatureIndexes[paper]))

	out = open("../metrics/featureWeightsHeuristic2.txt", "w")

	for feature in featureWeightsDict:
		featureWeightsDict[feature]	= featureWeightsDict[feature]/float(len(maxFeatureIndexes))
		out.write(str(feature) + "\t" + str(featureWeightsDict[feature]) + "\n")

	out.close()


def main():
	calculateHeuristic3()

if __name__ == '__main__':
	main()



