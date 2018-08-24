#!/usr/bin/python
'''USAGE: getSeqs.py BLAST_results fasta_file
Pulls out selected sequences from large fasta file based on tab-formatted blast results
'''
import sys

def readBlast():

	with open(sys.argv[1],'r') as blastOut:

		bestHits = []
		for line in blastOut:
			currHit = line.split()[0].replace('|','_')
			bestHits.append(currHit)

	return(bestHits)


names = readBlast()

reading = 0
all_read = 0
with open(sys.argv[2], 'r') as fasta:

	print('\n')
	for line in fasta:

		if reading == 1:
			print(line)
			reading = 0
			all_read += 1
			if len(names) == all_read:
				break
			continue

		elif line[0] == '>':
			name = line.strip().replace('>','').replace('|','_')
			if name in names:
				print(line.strip())
				reading = 1

