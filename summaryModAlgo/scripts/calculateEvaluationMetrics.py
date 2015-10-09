import os
import sys
import time

isSummary = False
factWeightsFolder = "contextFactWeights"
factMatrixFolder = "contextFactMatrix"
contextFolder = "contextFiles"
factPyramidFolder = "contextFactPyramids"

if (sys.argv[1] == "summary"):
	factWeightsFolder = "summaryFactWeights"
	factMatrixFolder = "summaryFactMatrix"
	contextFolder = "modOutput"
	factPyramidFolder = "summaryFactPyramids"
	isSummary = True


if (isSummary):
	os.system("python createFactMatrix.py " + factMatrixFolder + " " + contextFolder + " summary")
else:
	os.system("python createFactMatrix.py " + factMatrixFolder + " " + contextFolder + " n")
os.system("python calculateFactWeights.py " + factMatrixFolder + " " + factWeightsFolder)
os.system("python createPyramid.py " + factWeightsFolder + " " + factPyramidFolder)

		