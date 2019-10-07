#!/usr/bin/python
'''USAGE: fq2fa.py fastq
Converts a fastq to a fasta
'''
import sys

fasta = str(sys.argv[1]).rstrip('fastq') + 'fasta'
fasta = open(fasta, 'w')

with open(sys.argv[1], 'r') as fastq:

	current = 1
	for line in fastq:

		if current == 1:
			line = line.replace('@','>')
			line = line.replace(' ','|')
			fasta.write(line)
			current += 1
			continue

		elif current == 2:
			fasta.write(line + '\n')
			current += 1
			continue

		elif current == 4:
			current = 1
			continue

		else:
			current += 1

fasta.close()
