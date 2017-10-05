#!/usr/bin/env python
# USAGE: python formatIDX.py idxstats.tsv contigs file
# Reformats idxstats files for use in contig binning

import sys

out_file = str(sys.argv[1]).rstrip('tsvx')
out_file = open(out_file, 'w')

with open(sys.argv[1], 'r') as in_file:

	removed = 0
	for line in in_file:
		line = line.split()

		if int(line[2]) == 0:
			removed += 1
			continue
		else:
			entry = line[0] + '\t' + str(line[2]) + '\n'
			out_file.write(entry)

out_file.close()
print('Removed contigs: ' + str(removed))

