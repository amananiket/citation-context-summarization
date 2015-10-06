import os
import sys

for filename in os.listdir("single-paper-ann/"):
	if (filename[-3:] == 'ann'):
		
		# Move the facts files with extension to facts folder for evaluation purposes
		os.rename("single-paper-ann/"+filename, "facts/"+filename)

	else:
		os.rename("single-paper-ann/"+filename, ""+filename)		
		os.system("perl C-LexRank.pl 5 " + filename)
		