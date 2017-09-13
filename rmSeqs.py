#!/usr/bin/env python
# USAGE: python rmSeqs.py fasta length
# Writes sequences above a user defined length to a new fasta file

import sys

min_len = int(sys.argv[2])
out_fasta = str(sys.argv[1]).rstrip('fastn') + str(min_len) + '.fasta'
out_fasta = open(out_fasta, 'w')

with open(sys.argv[1], 'r') as in_fasta:

	included = 0
	skipped = 0
	seq = ''

	for line in in_fasta:

		if line == '\n':
			continue
		elif line[0] == '>' and seq == '':
			current_seq = line
			current_seq = current_seq.replace(' ', '_')
			continue
		elif line[0] == '>' and seq != '':
			if len(seq.strip()) >= min_len:
				seq = seq + '\n'
				out_fasta.write(current_seq)
				out_fasta.write(seq)
				included += 1
			else:
				skipped += 1
			seq = ''
			current_seq = line
			continue
		else:
			seq = seq + line.strip()
			continue

out_fasta.close()
print('Included sequences: ' + str(included))
print('Omitted sequences: ' + str(skipped))

