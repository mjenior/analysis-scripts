#!/usr/bin/env python
'''USAGE: screenBins2.py report.txt genes
Screens contig bins by minimum called gene based on geneStats.py summaries
'''

import sys

fasta = 'none'
keep = 0
remove = 0
outFile = open('rm_bins.sh', 'w')
with open(sys.argv[1], 'r') as inFile:
	for line in inFile:
		line = line.split()

		if len(line) == 0:
			continue
		elif line[0] == 'Fasta:':
			fasta = line[1]
			continue
		elif line[0] == 'Genes:':
			if int(line[1]) < int(sys.argv[2]): 
				blast = fasta.split('genes')[0] + 'KEGGprot.out'
				outFile.write('rm ' + blast + '\n')
				remove += 1
			else:
				keep += 1
			continue
		else:
			continue

outFile.close()
print('Saved bins:', keep)
print('Ignored bins:', remove)

