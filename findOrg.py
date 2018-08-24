#!/usr/bin/python
'''USAGE: findOrg.py BLAST_output.tsv
Finds the most abundant organism (KEGG) annotated in a tab formatted BLAST output
'''
import sys

# Read in KEGG organism codes
with open('/scratch/mj4pw/ref/kegg/kegg_organisms.tsv','r') as keggOrg:
        orgDict = {}
        for entry in keggOrg:
                orgDict[entry.split()[0]] = entry.split()[2]

# Read in BLAST hits and retreive organsim info
with open(sys.argv[1],'r') as blastOut:
	hitDict = {}
	hits = 0
	orgSet = set()
	for hit in blastOut:
		hits += 1
		org = hit.split()[1].split(':')[0]
		org = orgDict[org]
		if not org in orgSet:
			orgSet.add(org)
			hitDict[org] = 1
		else:
			hitDict[org] += 1

print('\nInput file: ' + str(sys.argv[1]))
print('Genes annotated: ' + str(hits))

# Find most abundant organism
mostHits = 0
for index in hitDict.keys():
	if hitDict[index] > mostHits:
		mostHits = hitDict[index]
		topOrg = index

percTop = (float(mostHits) / float(hits)) * 100.00
percTop = round(percTop, 2)

print('Most frequent hit: ' + topOrg)
print('Ratio of genes: ' + str(percTop) + '%\n')
