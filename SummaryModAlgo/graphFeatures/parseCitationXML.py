from bs4 import BeautifulSoup as BS 
import os
citations = []

for f in os.listdir("minimisedAAn/"):
	fileContent = open("minimisedAAn/" + f, "r")
	fileSoup = BS(fileContent, "xml")
	for cited in fileSoup.find("paper").findAll("cited"):
		citation = {}
		citation['id'] = cited['id']
		citation['citingPaper'] = cited.find("title")['id'][:-4]
		citation['citedPaper'] = cited.find("citsent")['citstr'].strip()
		citation['citationContext'] = cited.find("citsent").contents
		citations.append(citation)

	break

print citations


