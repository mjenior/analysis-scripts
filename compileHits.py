#!/usr/bin/python
# Compiles all unique genes found across multiple diamond blastp .out files listed in the input doc

import sys

with open(sys.argv[1], 'r') as inFiles:
	f = [x.strip() for x in inFiles.readlines()]

entryDict = {}
for x in f:
	if x != '':
		with open(x, 'r') as current:
			for line in current:
				if len(line) != 0:
					gene = line.split()[1]
					entryDict[gene] = line

with open(sys.argv[2], 'w') as outFile:
	total = 0
	for x in entryDict.keys():
		outFile.write(entryDict[x])
		total += 1

print('Total genes:', total)
