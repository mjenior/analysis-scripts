#!/usr/bin/python
'''USAGE: compileStats.py stats.txt
Reads, collates, and prints summary statistics for contig bin reports
'''
import sys

bins = []
excluded = []
included = []
percIncl = []
bases = []
medianLen = []
longestLen = []
shortestLen = []
with open(sys.argv[1], 'r') as inFile:

	for line in inFile:
		line = line.strip()
		if '_bins' in line:
			bins.append(line.rstrip('_bins'))
			continue

		line = line.split()

		if 'excluded:' in line:
			excluded.append(int(line[2]))
		elif 'included:' in line:
			included.append(int(line[2]))
		elif 'Percent' in line:
			percIncl.append(float(line[2].rstrip('%')))
		elif 'size:' in line:
			bases.append(float(line[3]))
		elif 'length:' in line:
			medianLen.append(int(line[3]))
		elif 'longest' in line:
			longestLen.append(int(line[3]))
		elif 'shortest' in line:
			shortestLen.append(int(line[3]))

bins = '\t'.join([str(x) for x in bins])
excluded = '\t'.join([str(x) for x in excluded])
included = '\t'.join([str(x) for x in included])
percIncl = '\t'.join([str(x) for x in percIncl])
bases = '\t'.join([str(x) for x in bases])
medianLen = '\t'.join([str(x) for x in medianLen])
longestLen = '\t'.join([str(x) for x in longestLen])
shortestLen = '\t'.join([str(x) for x in shortestLen])

with open('compiled.tsv', 'w') as outFile:
	outFile.write('bin\t' + bins + '\n')
	outFile.write('excluded_contings\t' + excluded + '\n')
	outFile.write('included_contigs\t' + included + '\n')
	outFile.write('percent_exclusion\t' + percIncl + '\n')
	outFile.write('total_bases\t' + bases + '\n')
	outFile.write('median_length\t' + medianLen + '\n')
	outFile.write('longest_length\t' + longestLen + '\n')
	outFile.write('shortest_length\t' + shortestLen + '\n')
