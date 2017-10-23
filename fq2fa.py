#!/usr/bin/python
'''USAGE: fq2fa.py fastq
Converts a fastq to a fasta
'''
import sys

fasta = str(sys.argv[1]).rstrip('fastq') + 'fasta'
fasta = open(fasta, 'w')

with open(sys.argv[1], 'r') as fastq:
	read = 0
	for line in fastq:
		if line[0] == '@'
			line = line.replace('@','>')
			fasta.write(line)
			read = 1
			continue
		elif read == 1
			fasta.write(line)
			read = 0

fasta.close()
