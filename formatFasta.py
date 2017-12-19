#!/usr/bin/python
'''USAGE: formatFasta.py fasta
Reformats fasta files to be uniform
'''
import sys

outFasta = str(sys.argv[1]).rstrip('fastnx') + 'format.fasta'
outFasta = open(outFasta, 'w')

with open(sys.argv[1], 'r') as inFasta:

	firstLine = inFasta.readline()
	firstLine = firstLine.replace(' ', '_').replace('|', '__').replace(',', '_')
	outFasta.write(firstLine)

	seq = ''
	for line in inFasta:

		if line[0] == '>':
				seq = seq.upper() + '\n\n'
				outFasta.write(seq)
				seq = ''
				
				line = line.replace(' ', '_').replace('|', '__').replace(',', '_')
				outFasta.write(line)
				continue
		else:
			seq += line.strip()

seq = seq.upper() + '\n\n'
outFasta.write(seq)
outFasta.close()
