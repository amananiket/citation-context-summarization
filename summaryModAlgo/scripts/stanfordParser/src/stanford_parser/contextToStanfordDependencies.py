import sys
import re
import os
import parser

def main():

	stanfordParser = parser.Parser()

	for f in os.listdir('../../../../contextFiles/'):

		with open('../../../../preProcessOutput/' + f[:-4] + "-tempSents.txt") as inputFile:
			
			inputLines = {}

			for line in inputFile:
				inputLines[int(line.split("\t")[0])] = 	line.split("\t")[1].decode('utf-8',"replace").strip('\n').lower()
			
			outputFile = open('../../../../stanfordDependencies/' + f, "w")

			
			for line in inputLines:
				lineText = inputLines[line]

				try:
					dependencies = stanfordParser.parseToStanfordDependencies(lineText)
					tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dependencies.dependencies]

					#print tupleResult
					
					outputFile.write(str(line) + "\t" + str(tupleResult) + "\n")

				except:
					print "No parse available."
					outputFile.write(str(line) + "\n")					



if __name__ == '__main__':
	main()