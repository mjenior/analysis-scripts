#!/usr/bin/python
'''USAGE: formatFasta.py fasta
Reformats fasta files to be uniform
'''
import sys

outFna = str(sys.argv[1]).rstrip('fastn') + 'format.fasta'
outFna = open(outFna, 'w')

with open(sys.argv[1], 'r') as inFna:

	seq = 'first'
	for line in inFna:
		if line == '\n':
			continue
		elif line[0] == '>':
			if seq != 'first':
				seq = seq.upper() + '\n\n'
				outFna.write(seq)
				seq = ''
			else:
				seq = ''
			entry = line.replace('   ', '\t')
			entry = entry.replace(' ', '_')
			entry = '__'.join(entry.split()) + '\n'
			outFna.write(entry)
		else:
			seq = seq + line.strip()

outFna.close()
