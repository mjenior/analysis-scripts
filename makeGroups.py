#!/usr/bin/python
'''USAGE: makeGroups.py fasta
Creates a groups file for a fasta
'''
import sys

group = str(sys.argv[1]).split('.')[0]
groups = group + '.groups'
groups = open(group, 'w')

with open(sys.argv[1], 'r') as fasta:
	for line in fasta:
		if line[0] != '>': continue

		seq = line.strip().lstrip('>')
		entry = seq + '\t' + group +'\n'
		groups.write(entry)

groups.close()

