#!/usr/bin/python
'''USAGE: renameFasta.py Fasta organism_name
Renames fasta file and sequences therein
'''
import sys

name = str(sys.argv[2])

outFasta = name + '.orf.pep.fasta'
outFasta = open(outFasta,'w')

with open(sys.argv[1],'r') as inFasta:
	genes = 0
	for line in inFasta:
		if line[0] != '>':
			outFasta.write(line)
			continue
		else:
			genes += 1
			entry = '>' + name + '__peptide__orf' + str(genes).zfill(5) + '\n'
			outFasta.write(entry)

outFasta.close()

