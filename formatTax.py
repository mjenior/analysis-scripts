#!/usr/bin/env python
# USAGE: formatTax.py taxonomy

import sys

outTax = str(sys.argv[1]).rstrip('taxonomy') + 'format.taxonomy'
outTax = open(outTax, 'w')
outTax.write('OTU\tSize\tTaxonomy\tGenera\n')

genusDict = {}
with open(sys.argv[1], 'r') as taxonomy:
	firstLine = taxonomy.readline()

	for line in taxonomy:
		line = line.split()

		otu = line[0]
		size = str(line[1])
		tax = line[2]
		genus = tax.rstrip(';').split(';')[-1]

		if not genus in genusDict.keys():
			genusDict[genus] = 1
			genus = genus + '[' + str(genusDict[genus]) + ']'
		else:
			genusDict[genus] += 1
			genus = genus + '[' + str(genusDict[genus]) + ']'

		entry = otu + '\t' + size + '\t' + tax + '\t' + genus + '\n'
		outTax.write(entry)

outTax.close()
