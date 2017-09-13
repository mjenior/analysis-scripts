#!/usr/bin/env python
# USAGE: python ASFcolor.py binned_fasta
# Creates color annotation file for ASF contig binning with Vizbin

import sys

color_dict = {'ASF356':'red\n', 'ASF360':'blue\n', 'ASF361':'green\n', 'ASF457':'yellow\n', 'ASF492':'orange\n', 'ASF500':'purple\n', 'ASF502':'cyan\n', 'ASF519':'black\n'}

label_file = str(sys.argv[1]).split('.')[0] + '.label'
label_file = open(label_file, 'w')
label_file.write('label\n')

with open(sys.argv[1], 'r') as binned_contigs:

	for line in binned_contigs:

		if line[0] == '>':
			member = line.split('_')[0]
			member = member.lstrip('>')
			label_file.write(color_dict[member])
			continue

		else:
			continue

label_file.close()