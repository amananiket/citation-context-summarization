import os
import sys



def main():

	with open("mappings.txt", "w") as mapping:

		## Baseline

		for filename in os.listdir("../../summaryModAlgo/contextFiles/"):
			mapping.write(" ".join([filename, "baselineCLexRank" ,"../../summaryModAlgo/contextFiles/"+filename, "../../summaryModAlgo/baselineSummary/"+filename[:-4]+"-C-LR.txt" + "\n"]))
		
		## Mod algorithm

		for filename in os.listdir("../../summaryModAlgo/contextFiles/"):
			mapping.write(" ".join([filename, "modCLexRank" ,"../../summaryModAlgo/contextFiles/"+filename, "../../summaryModAlgo/modOutput/"+filename[:-4]+"-C-LR.txt" + "\n"]))
	


if __name__ == '__main__':
	main()