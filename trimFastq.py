#!/usr/bin/python
'''USAGE: trimFastq.py fastq 250
Trims sequences and quality scores to a given length
'''
import sys

outFastq = str(sys.argv[1]).rstrip('fastq') + 'trim.fastq'
outFastq = open(outFastq, 'w')
seq_len = int(sys.argv[1])

with open(sys.argv[1], 'r') as inFastq:
	for line in inFastq:
		if line[0] == '@':
			outFastq.write(line)
			continue
		elif line.strip() == '+':
			outFastq.write(line)
			continue
		else:
			line = line[0:seq_len] + '\n'
			outFastq.write(line)
			
outFastq.close()

