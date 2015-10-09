import re
import codecs


def main():
	inputFile = open("../../../aan/release/2013/acl-metadata.txt", "r")

	paperIDList = {}
	paperAuthorsList = {}
	titlesList = {}
	yearsList = {}

	pattern = re.compile('{(.*)}')

	paperIndex = -1

	for line in inputFile:
		pair = line.decode("utf-8", "replace").split("=")

		if (len(pair) == 2):
			valueString = pair[1].strip()[1:-1]

			if (pair[0].strip() == "id"):
				paperIndex += 1
				paperIDList[paperIndex] = valueString.encode("utf-8")
			elif (pair[0].strip() == "author"):
				authors = valueString.encode("utf-8")
				authorsList = authors.split(";")
				paperAuthorsList[paperIndex] = authorsList
			elif (pair[0].strip() == "year"):
				yearsList[paperIndex] = int(valueString)
			elif (pair[0].strip() == "title"):
				titlesList[paperIndex] = valueString.encode("utf-8")

		

	print len(paperIDList), len(paperAuthorsList), len(titlesList), len(yearsList)
	authorsFile = open("../graphFeatures/authors.txt", "w")
	titlesFile = open("../graphFeatures/titles.txt", "w")
	yearsFIle = open("../graphFeatures/years.txt", "w")

	for i in range(0, paperIndex+1):
		if (i in paperAuthorsList):
			authorsFile.write(paperIDList[i] + "\t" + "\t".join(paperAuthorsList[i]) + "\n")
		if (i in titlesList):
			titlesFile.write(paperIDList[i] + "\t" + titlesList[i] + "\n")
		if (i in yearsList):
			yearsFIle.write(paperIDList[i] + "\t" + str(yearsList[i]) + "\n")


	authorsFile.close()
	titlesFile.close()
	yearsFIle.close()



if __name__ == "__main__":
	main()