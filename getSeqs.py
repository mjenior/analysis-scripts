#!/usr/bin/python
'''USAGE: getSeqs.py BLAST_results fasta_file
Pulls out selected sequences from large fasta file based on tab-formatted blast results
'''
import sys

bestHits = set()
with open(sys.argv[1],'r') as blastOut:

	for line in blastOut:
		bestHits |= set([line.split()[0]])

out_fasta = str(sys.argv[2]).rstrip('fastn') + 'filter.fasta'
out_fasta = open(out_fasta, 'w')

include_seq = 0
with open(sys.argv[2], 'r') as fasta:

	for line in fasta:

		if line[0] == '>':
			name = line.strip().replace('>','')
			if name in bestHits:
				out_fasta.write(line)
				include_seq = 1
				continue
		
		elif include_seq == 1:
			out_fasta.write(line)
			include_seq = 0

out_fasta.close()
