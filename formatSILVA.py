#!/usr/bin/env python
'''
USAGE: python formatSILVA.py silva.fasta
Untrascribes and reformates SILVA fasta files
'''

import sys

def untranscribe(rna):

	transDict = {'A':'T', 'U':'A', 'C':'G', 'G':'C', 'R':'Y',
	'Y':'R', 'S':'S', 'W':'W', 'K':'M', 'M':'K',
	'B':'V', 'D':'H', 'H':'D', 'V':'B', 'N':'N'}

	dna = ''
	for nuc in rna: dna += transDict[nuc]

	return ''.join(dna)


out_file = open(str(sys.argv[1]).rstrip('fastn') + 'format.fasta', 'w')
with open(sys.argv[1], 'r') as in_file:
	header = in_file.readline()
	header = header.split()
	taxa = '_'.join(header[1:])
	out_file.write(header[0] + '|' + taxa + '\n')

	seq = ''
	for line in in_file:
		if line[0] == '>':
			seq = untranscribe(seq)
			out_file.write(seq + '\n\n')
			seq = ''
			line = line.split()
			taxa = '_'.join(line[1:])
			out_file.write(header[0] + '|' + taxa + '\n')
		else:
			seq += line.strip()

seq = untranscribe(seq)
out_file.write(seq + '\n')
out_file.close()

