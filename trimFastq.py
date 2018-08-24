#!/usr/bin/python
'''USAGE: trimFastq.py fastq 250
Trims sequences and quality scores to a given length
'''
import sys

outFastq = str(sys.argv[1]).rstrip('fastq') + 'trim.fastq'
outFastq = open(outFastq, 'w')
#seqLen = int(sys.argv[2])
seqLen = 250

with open(sys.argv[1], 'r') as inFastq:
	curr = 1
	for line in inFastq:
		if curr == 1:
			outFastq.write(line)
			curr += 1
			continue
		elif curr == 2:
			line = line[0:seqLen] + '\n'
			outFastq.write(line)
			curr += 1
			continue
		elif curr == 3:
			outFastq.write(line)
			curr += 1
			continue
		elif curr == 4:
			line = line[0:seqLen] + '\n'
			outFastq.write(line)
			curr = 1
			continue
			
outFastq.close()

