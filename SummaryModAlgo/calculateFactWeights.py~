import os
import sys

for filename in os.listdir(sys.argv[1] + '/'):
		output = open(sys.argv[2] + '/'+filename,'w')
		fact_matrix_file = open(sys.argv[1] + '/'+filename,'r')
		weight = {}
		for line in fact_matrix_file:
			line = line.rstrip().split('\t')
			for i in range(0,len(line)):
				if i  not in weight:
					weight[i] = int(line[i])
				else:
					weight[i] += int(line[i])
		
		
		for w in weight:
			output.write(str(w+1)+'\t'+str(weight[w])+'\n')
		
