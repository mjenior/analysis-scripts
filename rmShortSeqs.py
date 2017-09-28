#!/usr/bin/env python
# USAGE: python rmShortSeqs.py fasta length
# Writes sequences above a user defined length to a new fasta file

import sys

min_len = int(sys.argv[2])
out_fasta = str(sys.argv[1]).rstrip('fastn') + str(min_len) + '.fasta'
out_fasta = open(out_fasta, 'w')

with open(sys.argv[1], 'r') as in_fasta:

	include = 0
	skip = 0
	curr_name = in_fasta.readline().replace(' ', '|')
	curr_seq = ''

	for line in in_fasta:

		if line[0] == '>':
			if len(curr_seq) >= min_len:
				out_fasta.write(curr_name)
				curr_seq = curr_seq + '\n\n'
				out_fasta.write(curr_seq)
				include += 1
			else:
				skip += 1
			curr_name = line.replace(' ', '|')
			curr_seq = ''
		else:
			curr_seq = curr_seq + line.strip()

	if len(curr_seq) >= min_len:
		out_fasta.write(curr_name)
		curr_seq = curr_seq + '\n\n'
		out_fasta.write(curr_seq)
		include += 1
	else:
		skip += 1


out_fasta.close()
print('Included sequences: ' + str(include))
print('Omitted sequences: ' + str(skip))

