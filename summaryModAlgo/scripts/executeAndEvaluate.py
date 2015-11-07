import os
import sys
import time


startTime = time.time()

## "2 arguments required. Format :  python executeAndEvalute.py <featureIndex> <comments>"

if ((int(sys.argv[1]) > 0 and int(sys.argv[1]) <= 10) or  int(sys.argv[1]) == 13):
	os.system("python executeModAlgo.py " + sys.argv[1] + " " + sys.argv[3])	
else:
	os.system("python executeModAlgo.py " + sys.argv[1] + " " + sys.argv[3] + " "  + sys.argv[4] ) 
os.system("python calculateEvaluationMetrics.py summary")
os.system("python calculatePScore.py '"+sys.argv[2] + "'")	
endTime = time.time()

print "\n\nTime elapsed = " + str(endTime - startTime) + " seconds"
