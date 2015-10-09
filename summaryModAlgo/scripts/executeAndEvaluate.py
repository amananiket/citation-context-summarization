import os
import sys
import time


startTime = time.time()

## "2 arguments required. Format :  python executeAndEvalute.py <featureIndex> <comments>"
	
os.system("python executeModAlgo.py " + sys.argv[1] )
os.system("python calculateEvaluationMetrics.py summary")
os.system("python calculatePScore.py '"+sys.argv[2] + "'")	
endTime = time.time()

print "\n\nTime elapsed = " + str(endTime - startTime) + " seconds"