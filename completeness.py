#!/usr/bin/python2.7
'''USAGE: completeness.py BLAST_output (tab formatted)
Prints % completeness based on marker gene BLAST of caled genes from a genome
Markers from Lan et al. (2016)
'''
import sys

with open(sys.argv[1],'r') as blastOut:

	geneHits = []
	orgHits = []
	hits = 0.0
	for line in blastOut:
		hits += 1.0
		currHit = line.split()[1]
		currGene = currHit.split('_')[-1]
		currOrg = currHit.split('_')[0]
		geneHits.append(currGene)
		orgHits.append(currOrg)


uniqueGenes = list(set(geneHits))
multiHits = []
for index in uniqueGenes:
	if geneHits.count(index) >= 2:
		multiHits.append(geneHits.count(index))
contamination = (float(sum(multiHits)) / hits) * float(len(multiHits))
contamination = round((contamination * 100.0), 2)

uniqueGenes = float(len(uniqueGenes))
completeness = round(((uniqueGenes / 73.0) * 100.0), 2)

uniqueOrgs = list(set(orgHits))
topCount = 0
hitCounts = []
topOrg = 'org'
for index in uniqueOrgs:
	if orgHits.count(index) > topCount:
		topCount = orgHits.count(index)
		hitCounts.append(topCount)
		topOrg = index

otherCount = float(hits - topCount)
uniqueOrgs = float(len(uniqueOrgs))
heterogeneity = (otherCount / float(hits)) * uniqueOrgs
heterogeneity = round((heterogeneity * 100.0), 2)


print('\nGenome bin: ' + str(sys.argv[1]))
print('Completeness: ' + str(completeness) + '%')
print('Contamination: ' + str(contamination) + '%')
print('Heterogeneity: ' + str(heterogeneity) + '%\n')


