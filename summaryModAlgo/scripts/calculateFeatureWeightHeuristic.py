
def main():
	
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

	



if __name__ == '__main__':
	main()



