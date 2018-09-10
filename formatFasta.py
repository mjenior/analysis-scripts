#!/usr/bin/python
'''USAGE: formatFasta.py fasta
Reformats fasta files to be uniform
'''
import sys

suffix = str(sys.argv[1]).split('.')[-1]
outFasta = str(sys.argv[1]).rstrip('fastnx') + 'format.' + suffix
outFasta = open(outFasta, 'w')

with open(sys.argv[1], 'r') as inFasta:

	firstLine = inFasta.readline()
	firstLine = firstLine.replace(' ', '_').replace('|', '__').replace(',', '.')
	outFasta.write(firstLine)

	seq = ''
	for line in inFasta:

		if line[0] == '>':
			seq = seq.upper() + '\n\n'
			outFasta.write(seq)
			seq = ''
			
			line = line.replace(' ', '_').replace('|', '__').replace(',', '.')
			outFasta.write(line)
			continue
		else:
			seq += line.strip()

seq = seq.upper() + '\n\n'
outFasta.write(seq)
outFasta.close()
