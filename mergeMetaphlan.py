#!/usr/bin/python
'''USAGE: mergeMetaphlan.py sample_name
Merges Metaphlan2 output from paired read files
'''
import sys
import numpy

sample_name = str(sys.argv[1])
taxons = set()

sample1_dict = {}
sample1 = sample_name + '_1.metaphlan2.out'
with open(sample1, 'r') as inFile:
	header = inFile.readline()
	for line in inFile:
		line = line.split()
		taxons |= set([line[0]])
		sample1_dict[line[0]] = float(line[1])

sample2_dict = {}
sample2 = sample_name + '_2.metaphlan2.out'
with open(sample2, 'r') as inFile:
	header = inFile.readline()
	for line in inFile:
		line = line.split()
		taxons |= set([line[0]])
		sample2_dict[line[0]] = float(line[1])


taxLvls = []
merged_dict = {}
for tax in taxons:
	taxLvls.append(len(tax.split('|')))

	try:
		abund1 = sample1_dict[tax]
	except KeyError:
		abund1 = 0.
	try:
		abund2 = sample2_dict[tax]
	except KeyError:
		abund2 = 0.

	if abund1 == 0. and abund2 == 0.:
		continue
	else:
		medAbund = round(numpy.median([abund1, abund2]), 3)
		merged_dict[tax] = [str(abund1), str(abund2), str(medAbund)]
		

level_dict = {1:['kingdom','kingdom'], 2:['phylum','kingdom\tphylum'], 3:['class','kingdom\tphylum\tclass'], 4:['order','kingdom\tphylum\tclass\torder'], 5:['family','kingdom\tphylum\tclass\torder\tfamily'], 6:['genus','kingdom\tphylum\tclass\torder\tfamily\tgenus'], 7:['species','kingdom\tphylum\tclass\torder\tfamily\tgenus\tspecies'], 8:['subspec','kingdom\tphylum\tclass\torder\tfamily\tgenus\tspecies\tsubspec']}

for lvl in range(1, max(taxLvls)+1):
	taxon = level_dict[lvl][0]
	header = level_dict[lvl][1] + '\tmedian_relabund\n'
	current = sample_name + '.' + taxon + '.merged.metaphlan2.tsv'
	with open(current, 'w') as outFile:
		outFile.write(header)
		for x in merged_dict.keys():
			if not 'k__Bacteria' in x:
				continue
			
			taxs = x.split('|')
			taxs = [y.split('__')[1] for y in taxs]
			if len(taxs) == lvl:
				entry = '\t'.join(taxs) + '\t' + merged_dict[x][2] + '\n'
				outFile.write(entry)

