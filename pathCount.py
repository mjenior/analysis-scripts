#!/usr/bin/python
'''USAGE: pathCount.py BLASToutput
Finds abundance of KEGG pathway annotations in a tsv formatted BLAST output
'''
import sys

# Write dictionary from BLAST output
with open(sys.argv[1],'r') as blast:
	pathDict = {}
	totalHits = 0
	metabolicHits = 0
	for line in blast:
		totalHits += 1
		entry = line.split()[1]
		paths = entry.split('|')[-1].split(';')
		if paths[0] == 'no_pathway_id':
			continue
		paths = list(set(paths))
		if 'Metabolic_pathways' in paths:
			metabolicHits += 1
			for index in paths:
				if not index in pathDict.keys():
					pathDict[index] = 1
				else:
					pathDict[index] += 1

firstPerc = 0.0
firstPath = 'index'
secondPerc = 0.0
secondPath = 'index'
thirdPerc = 0.0
thirdPath = 'index'
for index in pathDict.keys():
	hitPerc = round(((float(pathDict[index]) / float(metabolicHits)) * 100.00), 2)
	print(index + '\t' + str(hitPerc) + '%')
	if hitPerc > firstPerc and index != 'Metabolic_pathways':
		thirdPerc = secondPerc
		thirdPath = secondPath
		secondPerc = firstPerc
		secondPath = firstPath
		firstPerc = hitPerc
		firstPath = index


print('\nTotal annotated genes: ' + str(totalHits) + '\n')
print('Annotated as Metabolic_pathways: ' + str(metabolicHits))
print('Most annotated sub-category: ' + str(firstPath) + '\t' +  str(firstPerc) + '%')
print('2nd most annotated sub-category: ' + str(secondPath) + '\t' +  str(secondPerc) + '%')
print('3rd most annotated sub-category: ' + str(thirdPath) + '\t' +  str(thirdPerc) + '%' + '\n')


