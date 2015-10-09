
inputFile = open("../../../aan/release/2013/acl.txt", "r")
outputFile = open("../graphFeatures/edgesAAN.txt", "w")

for line in inputFile:
	citingPaper = line.split("==>")[0].strip()
	citedPaper = line.split("==>")[1].strip()
	outputFile.write(citingPaper + "\t" + citedPaper + "\n")

