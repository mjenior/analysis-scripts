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

	accepted = []
	print('')
	for line in checkm:
		line = line.split()
		# Last line
		if len(line) == 0:
			continue
		# Header
		elif line[0] == 'Bin_Id':
			continue
		# Not able to classify
		elif line[1].split('(')[0] == 'root':
			print('Rejected: ' + line[0])
			continue
		# Only kingdom level classification
		elif line[1].split('__')[0] == 'k':
			print('Rejected: ' + line[0])
			continue
		# Number of genomes hit against
		elif int(line[2]) >= 5000:
			print('Rejected: ' + line[0])
			continue
		# Completeness
		elif float(line[11]) <= 40.0:
			print('Rejected: ' + line[0])
			continue
		# Contamination
		elif float(line[12]) >= 33.333:
			print('Rejected: ' + line[0])
			continue
		else:
			prevName = line[0] + '.fa'
			newName = line[1].split('__')[1] + '.' + str(line[11]) + '.contigs.fasta'
			entry = prevName + ' --> ' + newName
			accepted.append(entry)
			newName = directory + '/' + line[1].split('__')[1] + '.' + str(line[11]) + '.contigs.fasta'
			os.rename(prevName, newName)

print('\nAccepted:')
for index in accepted:
	print(index)