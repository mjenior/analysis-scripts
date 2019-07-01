#!/usr/bin/python

import sys

outFastq = str(sys.argv[1]).rstrip('fastq') + 'reduced.fastq'
outFastq = open(outFastq, 'w')

cutoff = int(sys.argv[2])

with open(sys.argv[1], 'r') as inFastq:

	currLine = 1
	totalEntries = 0
	read = 0

	for line in inFastq:
		currLine += 1
        outFastq.write(line)

        if line_count == 5:
        	totalEntries += 1
        	currLine = 1

        if totalEntries == cutoff:
        	outFastq.close()
        	break
