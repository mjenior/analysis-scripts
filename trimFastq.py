#!/usr/bin/python
'''USAGE: trimFastq.py fastq
Trims sequences and quality scores to a given length
'''
import sys

outFastq = str(sys.argv[1]).rstrip('fastq') + 'trim.fastq'
outFastq = open(outFastq, 'w')

with open(sys.argv[1], 'r') as inFastq:
	for line in inFastq:
		if line[0] in ['@', '+']:
			outFastq.write(line)
			continue
		else:
			line = line[0:250] + '\n'
			outFastq.write(line)
			
outFastq.close()

