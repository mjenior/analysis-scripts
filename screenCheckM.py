#!/usr/bin/python
'''USAGE: screenCheckM.py bin_quality_table
Checks quality of genome bins and collects most useable OGUs
'''
import sys
import os

# Create and navigate to new output directory
directory = str(os.getcwd()) + '/screened_bins'
os.makedirs(directory)

with open(sys.argv[1], 'r') as checkm:

	for line in checkm:
		line = line.split()
		if len(line) == 0:
			continue
		elif line[0] == 'Bin_Id':
			continue
		elif line[1].split('(')[0] == 'root':
			continue
		elif line[1].split('__')[0] == 'k':
			continue
		elif int(line[2]) <= 5449:
			continue
		elif float(line[11]) <= 40.0:
			continue
		elif float(line[12]) >= 33.333:
			continue
		else:
			prevName = line[0] + '.fa'
			newName = 'screened_bins/' + line[1].split('__')[1] + '.' + str(line[11]) + '.contigs.fasta'
			os.rename(prevName, newName)

