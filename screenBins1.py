#!/usr/bin/env python
'''USAGE: screenBins.py report.txt size
Screens contig bins by minimum size based on contigStats.py out summaries
'''

import sys

assembly = 'none'
keep = 0
remove = 0
outFile = open('rm_bins.sh', 'w')
with open(sys.argv[1], 'r') as inFile:
	for line in inFile:
		line = line.split()

		if len(line) == 0:
			continue
		elif line[0] == 'Assembly:':
			assembly = line[1]
			continue
		elif line[0] == 'Bases(Mb):':
			if float(line[1]) <= float(sys.argv[2]): 
				outFile.write('rm ' + assembly + '\n')
				keep += 1
			else:
				remove += 1
			continue
		else:
			continue

outFile.close()
print('Saved bins:', keep)
print('Ignored bins:', remove)
