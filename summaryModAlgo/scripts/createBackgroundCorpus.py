def main():

	outfile = open("../../SIMetrix-v1/data/CLexRankBgFreqCounts.unstemmed.txt", "w")

	with open("../IDFMetrics/idf.txt", "r") as freqCounts:
		for line in freqCounts:
			outfile.write(" ".join(line.split("\t")))


if __name__ == '__main__':
	main()