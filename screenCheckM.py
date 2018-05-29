#!/usr/bin/python
'''USAGE: screenCheckM.py bin_quality_table
Checks quality of genome bins and collects most useable OGUs
'''
import sys
import os

# Create and navigate to new output directory
directory = str(os.getcwd()) + '/screened_bins'
if not os.path.exists(directory):
	os.makedirs(directory)

with open(sys.argv[1], 'r') as checkm:

	for line in checkm:
		line = line.split()
		if len(line) == 0:
			print('test1')
			continue
		elif line[0] == 'Bin_Id':
			print('test2')
			continue
		elif line[1].split('(')[0] == 'root':
			print('test3')
			continue
		elif line[1].split('__')[0] == 'k':
			print('test4')
			continue
		elif int(line[2]) >= 5449:
			print('test6')
			continue
		elif float(line[11]) >= 40.0:
			print('test7')
			continue
		elif float(line[12]) <= 33.333:
			print('test8')
			continue
		else:
			print('test9')
			prevName = line[0] + '.fa'
			newName = directory + '/' + line[1].split('__')[1] + '.' + str(line[11]) + '.contigs.fasta'
			os.rename(prevName, newName)
