#!/usr/bin/python
'''USAGE: findUID.py BLAST_output.tsv
Finds most abundant organism annotation from marker gene BLAST (Lan et al. 2016)
'''
import sys


# Read in BLAST hits
with open(sys.argv[1], 'r') as blastOut:
	hitDict = {}
	hitSet = set()
	hits = 0
	for hit in blastOut:
		hits += 1
		hit = hit.split()[1].split('_')[0]
		if not hit in hitSet:
			hitSet.add(hit)
			hitDict[hit] = 1
			continue
		else:
			hitDict[hit] += 1


# Find most abundant UID
mostHits = 0
for index in hitDict.keys():
	if hitDict[index] > mostHits:
		mostHits = hitDict[index]
		topOrg = index
percTop = (float(mostHits) / float(hits)) * 100.00
percTop = round(percTop, 2)


# Print results
print('\nInput file: ' + str(sys.argv[1]))
print('Most frequent hit: ' + topOrg)
print('Ratio of hits: ' + str(percTop) + '%\n')

