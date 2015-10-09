import os
import sys
import random

for filename in os.listdir("../contextFiles/"):
	with open("../contextFiles/" + filename, "r") as inputFile:
		inputLines = [x.strip('\n') for x in inputFile.readlines()]
		randomOutputLines = random.sample(set(inputLines), 5)

		randomOutputTrimmed = []
		wordCount = 0

		for line in randomOutputLines:
			wordCount += len(line.split())
			randomOutputTrimmed.append(line)
			if (wordCount >= 100):
				break

		output = open("../modOutput/" + filename[:-4] + "-C-LR.txt", "w")
		output.write("\n".join(randomOutputTrimmed))

	

os.system("python calculateEvaluationMetrics.py summary")
os.system("python calculatePScore.py 'Baseline setup: Random summary ~100 words'")
