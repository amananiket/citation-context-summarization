import os
import sys

def p_score():
	total_count = 0
	avg_p_score = 0.0

			
	logFile = open("log.txt", "a+")
	logFile.write("\n\n"+sys.argv[1] + "\n\n")
	for filename in os.listdir('contextFactPyramids/'):
			total_weight = 0
			total_count += 1
			fact_weights = open('contextFactWeights/'+filename,'r')
			fact_weight = {}		
			for line in fact_weights:
				line = line.rstrip().split('\t')
				fact_weight[line[0]] = int(line[1])
				total_weight += int(line[1])
			#print total_weight
			
			# Same as the file factWeights

			fact_matrix_file = open('summaryFactMatrix/'+filename[:-4]+'-C-LR.txt','r')
			weight = {}
			for line in fact_matrix_file:
				line = line.rstrip().split('\t')
				for i in range(0,len(line)):
					if i  not in weight:
						weight[i] = int(line[i])
					else:
						weight[i] += int(line[i])
	
			summary_weight = 0
			total_facts = 0
			for w in weight:
				if weight[w] > 0:
					summary_weight = summary_weight + fact_weight[str(w+1)]
					total_facts += 1
			
			#print "weight: ", weight
			#print 'summary_weight : ', summary_weight
			#print 'total_facts : ',total_facts			
			
			#fact_matrix_file = open('factPyramids/'+filename,'r')
			#count = 0 
			#sum = 0
			#for line in fact_matrix_file:
			#	line  = line.rstrip().split('\t')
			#	rem = total_facts  - count
			#	if rem > 0:
			#		length = len(line[1].split(','))
			#		if length <= rem:
			#			sum = sum + length*int(line[0])
			#			count  = count + length
			#		else:
			#			sum = sum + rem*int(line[0])
			#			count  =  count + rem

			#print sum
			#changed print filename, summary_weight/float(sum), summary_weight/float(total_weight) 
			logFile.write(filename + "\t" + str(summary_weight/float(total_weight)) + "\n")
			print filename, str(summary_weight/float(total_weight))
			#changed avg_p_score  += summary_weight/float(sum)
			avg_p_score  += summary_weight/float(total_weight)
			#return 

	print 'Pyramid Score = \t',avg_p_score/total_count
	logFile.write('\n\nPyramid Score = \t'+str(avg_p_score/total_count)+ "\n")

if __name__ == "__main__":
	p_score()
