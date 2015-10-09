from bs4 import BeautifulSoup as BS 
import os
citations = []

paperNames = []

for f in os.listdir("../contextFiles/"):
	paperNames.append(f[:-4])

print paperNames

outFile = open("../graphFeatures/citationGraphValues.txt", "w")

for f in os.listdir("../graphFeatures/minimisedAAn/"):
	fileContent = open("../graphFeatures/minimisedAAn/" + f, "r")
	fileSoup = BS(fileContent, "xml")
	for cited in fileSoup.find("paper").findAll("cited"):
		citation = {}
		try:
			citation['id'] = cited['id']
			citation['citingPaperTitle'] = cited.find("title").contents
			citation['citingPaper'] = cited.find("title")['id'][:-4]
			citation['citedPaper'] = cited.find("citsent")['citstr'].strip()
			citation['citationContext'] = cited.find("citsent").contents

			if (citation['citedPaper'] in paperNames):
				outFile.write(str(citation['id']) + "\t" + str(citation['citingPaper']) + "\t" +  str(citation['citingPaperTitle']) + "\t" + str(citation['citedPaper']) + "\t" + str(citation['citationContext']) + "\n")
				print citation['citingPaper'], citation['citingPaperTitle']
			citations.append(citation)
		except:
			print "Error in citation context parsing. Moving to the next one."




