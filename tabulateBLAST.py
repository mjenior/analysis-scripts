#!/usr/bin/python
'''USAGE: tabulateBLAST.py BLAST_results count_table
Counts instances of ref hits in tab-formatted BLAST output
'''

import sys

blastHit_dict = {}
with open(sys.argv[1], 'r') as blast:

	for line in blast:
		hit = line.split()[1]

		if not hit in blastHit_dict.keys():
			blastHit_dict[hit] = 1
		else:
			blastHit_dict[hit] += 1

with open(sys.argv[2], 'w') as outFile:

	for index in blastHit_dict.keys():
		line = index + '\t' + str(blastHit_dict[index]) + '\n'
		outFile.write(line)
