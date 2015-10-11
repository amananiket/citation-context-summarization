import os
import sys
import time

try:
	os.system("perl preProcess.pl 5 ../contextFiles/" + sys.argv[1] + ".txt")
	os.system("python calculateNodeSim.py " + sys.argv[1] + " " +sys.argv[2])
	os.system("perl C-LexRankMod.pl 5 ../contextFiles/" + sys.argv[1] + ".txt")
	
except:
	for filename in os.listdir("../contextFiles/"):
		os.system("perl preProcess.pl 5 ../contextFiles/" + filename)
		os.system("python calculateNodeSim.py " + filename[:-4] + " " + sys.argv[1])
		os.system("perl C-LexRankMod.pl 5 ../contextFiles/" + filename)

		
