import os
import numpy
from sklearn.preprocessing import normalize

nodes = []

for f in os.listdir("../contextFiles/"):
	nodes.append(f[:-4])

graphValuesFile = open("../graphFeatures/citationGraphValues.txt", "r")
nodesListOutput = open("../graphFeatures/nodesList.txt", "w")

for edge in graphValuesFile:
	if (str(edge.split("\t")[1]) not in nodes):
		nodes.append(str(edge.split("\t")[1]))

for node in nodes:
	nodesListOutput.write(str(nodes.index(node)) + "\t" + node + "\n")

adjacencyArray = numpy.zeros(shape=(len(nodes), len(nodes)))

graphValuesFile = open("../graphFeatures/citationGraphValues.txt", "r")
for edge in graphValuesFile:
	adjacencyArray[nodes.index(str(edge.split("\t")[1]))][nodes.index(str(edge.split("\t")[3]))] += 1
	#print nodes.index(str(edge.split("\t")[1])), nodes.index(str(edge.split("\t")[3]))

#print adjacencyMatrix
adjacencyMatrix = numpy.matrix(adjacencyArray)
adjacencyMatrixT = adjacencyMatrix.transpose()
bibilographicCoupling = numpy.dot(adjacencyMatrix, adjacencyMatrixT)
coCitationMatrix = numpy.dot(adjacencyMatrixT, adjacencyMatrix)

#print bibilographicCoupling
#print coCitationMatrix

bbCNormalized = normalize(bibilographicCoupling, axis = 1, norm = 'l1')
coCitNormalized = normalize(coCitationMatrix, axis = 1, norm = 'l1')

print bbCNormalized
print coCitNormalized
