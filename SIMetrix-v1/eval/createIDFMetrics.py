import os
import sys
import re
import math
from nltk import word_tokenize


word_dict = {}
df_dict = {}
N = 0
DOCS_BASE_DIR = "../../../aan/papers_text/"

def clean_text(raw):
	mod = ''.join(e for e in raw if e.isalnum() or e == ' ')
	mod = re.sub(r'\s+', ' ', mod)

	return mod

def create_word_dict():

	global word_dict, df_dict, DOCS_BASE_DIR, N

	for f in os.listdir(DOCS_BASE_DIR):

		if (f[-3:] == "txt"):

			N += 1

			doc_tokens = []

			with open(DOCS_BASE_DIR + f, "r") as inFile:
				inputLines = [x.decode('utf-8',"replace").strip('\n').lower() for x in inFile.readlines()]

				for line in inputLines:
					clean_line = clean_text(line)
					tokens = word_tokenize(clean_line)

					for token in tokens:
						if token not in word_dict:
							word_dict[token] = 1
						else:
							word_dict[token] += 1

					doc_tokens.extend(tokens)

			doc_tokens = set(doc_tokens)
			for token in doc_tokens:
				if token not in df_dict:
					df_dict[token] = 1
				else:
					df_dict[token] += 1


			print doc_tokens
			print "-----------------------------------"

def dump_metrics_to_file():

	global word_dict, df_dict, N

	with open("../data/AANbgFreqCounts.unstemmed.txt", "w") as freqDictFile:
		for token in word_dict:
			freqDictFile.write(" ".join([token.encode('utf-8'), str(word_dict[token])]) + "\n")

	with open("../data/AANbgIdfValues.unstemmed.txt", "w") as idfFile:

		idfFile.write(str(N) + "\n")

		for token in df_dict:
			idfFile.write(" ".join([token.encode('utf-8'), str(math.log(N/(1+float(df_dict[token]))))]) + "\n")







def main():
	create_word_dict()
	dump_metrics_to_file()
	


if __name__ == '__main__':
	main()