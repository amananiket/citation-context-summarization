import os
import sys

for filename in os.listdir("contextFiles/"):
	os.system("perl C-LexRankBaseline.pl 5 contextFiles/" + filename)
	

os.system("python calculateEvaluationMetrics.py summary")
os.system("python calculatePScore.py 'Baseline setup: C-LexRank algorithm on 5 sentences'")