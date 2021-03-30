#!/usr/bin/python

import sys

outFile = str(sys.argv[1]).rstrip('fastn') + 'fix.fasta'
outFile = open(outFile, 'w')

with open(sys.argv[1], 'r') as inFile:

	for line in inFile:
		if line[0] == '>':
			entry = line.split('>')[-1].replace('__','|')
			newLine = '>' + entry
			outFile.write(newLine)
		else:
			outFile.write(line)

outFile.close()
