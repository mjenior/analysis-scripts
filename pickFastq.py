#!/usr/bin/python
'''
USAGE: python pichFastq.py fastq sub_level
Returns a fastq file with the user provided number of subsampled reads
'''
import sys

outFastq = str(sys.argv[1]).rstrip('fastq') + 'pick.fastq'
outFastq = open(outFastq, 'w')

subLvl = int(sys.argv[2]) * 4

with open(sys.argv[1], 'r') as inFastq:

	current = 0
	for line in inFastq:
		current += 1
		outFastq.write(line)
		if current == subLvl:
			break

outFastq.close()
