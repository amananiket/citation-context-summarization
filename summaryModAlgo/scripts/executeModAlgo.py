import os
import sys
import time


try:
	option = int(sys.argv[1])
	for filename in os.listdir("../contextFiles/"):
		os.system("perl preProcess.pl 5 ../contextFiles/" + filename)
		if ((option <= 10 and option >0) or option == 13):
			os.system("python calculateNodeSim.py " + filename[:-4] + " " + sys.argv[1] + " "+ sys.argv[2])
		else:
			os.system("python calculateNodeSim.py " + filename[:-4] + " " + sys.argv[1] + " '"+sys.argv[2]+ "' " +sys.argv[3])  
		os.system("perl C-LexRankMod.pl 5 ../contextFiles/" + filename)


except:
	os.system("perl preProcess.pl 5 ../contextFiles/" + sys.argv[1] + ".txt")
	os.system("python calculateNodeSim.py " + sys.argv[1] + " " +sys.argv[2])
	os.system("perl C-LexRankMod.pl 5 ../contextFiles/" + sys.argv[1] + ".txt")
	