#!/usr/bin/python
'''USAGE: getSeqs.py --blast BLAST_results --fasta fasta_file --out screened_fasta --include True
Pulls out selected sequences from large fasta file based on tab-formatted blast results
'''
import sys
import argparse

# User defined arguments
parser = argparse.ArgumentParser(description='Screen Fasta files based on BLAST hits')
parser.add_argument('--blast', default='default', help='Tab-formatted BLAST output file')
parser.add_argument('--fasta', default='default', help='Fasta file to be screened')
parser.add_argument('--out', default='default', help='Name of output fasta file')
parser.add_argument('--include', default=True, help='Include or exclude those sequences found in BLAST file (True of False)')

args = parser.parse_args()
blast_file = str(args.blast)
fasta_file = str(args.fasta)
out_fasta = str(args.out)
keep = args.include

if blast_file == 'default' or fasta_file == 'default':
	raise NameError('Required input files not provided')

if out_fasta == 'default':
	out_fasta = str(out_fasta).rstrip('fastn') + 'keep.fasta'
out_fasta = open(out_fasta, 'w')

bestHits = set()
with open(blast_file, 'r') as blastOut:
	for line in blastOut: bestHits |= set([line.split()[0]])

include_seq = 0
with open(fasta_file, 'r') as fasta:

	for line in fasta:

		if line[0] == '>':
			name = line.strip().replace('>','')

			if keep != True:
				if not name in bestHits:
					out_fasta.write(line)
					include_seq = 1
					continue
			else:
				if name in bestHits:
				out_fasta.write(line)
				include_seq = 1
				continue
		
		elif include_seq == 1:
			out_fasta.write(line)
			include_seq = 0

out_fasta.close()
