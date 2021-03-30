#!/usr/bin/python

import sys
from numpy import median

def readAbund(file_name):

	abund_dict = {}
	with open(file_name, 'r') as abundances:
		header = abundances.readline()
		for line in abundances:
			line = line.split()
			abund_dict[line[0]] = float(line[1])

	return abund_dict


all_abund = {}
all_taxa = set()
all_samples = []
with open(sys.argv[1], 'r') as inFile:
	for line in inFile:

		temp_file = line.strip()
		temp_abund = readAbund(temp_file)
		temp_sample = 'fmt' + temp_file.split('.')[0]

		all_abund[temp_sample] = temp_abund
		all_taxa |= set(list(temp_abund.keys()))
		all_samples.append(temp_sample)


all_taxa = list(all_taxa)
all_samples = list(set(all_samples))
with open(sys.argv[2], 'w') as outFile:

	header = 'sample\t' + '\t'.join(all_taxa) + '\n'
	outFile.write(header)
	for x in all_samples:
		curr_abund = all_abund[x]
		curr_entry = x
		for y in all_taxa:
			curr_entry += '\t'
			try:
				z = curr_abund[y]
			except:
				z = 0.0
			curr_entry += str(z)
		curr_entry += '\n'
		outFile.write(curr_entry)

