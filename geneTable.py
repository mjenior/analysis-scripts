#!/usr/bin/python
'''USAGE: geneTable.py pooled_reports output.tsv
This script separates pooled assembly quality statistics into distinct tables
'''
import sys

with open(sys.argv[1], 'r') as report:

	fastas = ['Fastas']
	genes = ['Contigs']
	residues = ['Residues']
	medians = ['Median']
	q1 = ['Q1']
	q3 = ['Q3']
	iqr = ['IQR']
	means = ['Mean']
	std = ['Std']
	shortest = ['Shortest']
	longest = ['Longest']

	for line in report:

		if line == '\n':
			continue

		line = line.split()
		if line[0] == 'Fasta:':
			fastas.append(str(line[1]))
			continue
		elif line[0] == 'Genes:':
			genes.append(str(line[1]))
			continue
		elif line[0] == 'Residues:':
			residues.append(str(line[1]))
			continue
		elif line[0] == 'Median:':
			medians.append(str(line[1]))
			continue
		elif line[0] == 'Q1:':
			q1.append(str(line[1]))
			continue
		elif line[0] == 'Q3:':
			q3.append(str(line[1]))
			continue
		elif line[0] == 'IQR:':
			iqr.append(str(line[1]))
			continue
		elif line[0] == 'Mean:':
			means.append(str(line[1]))
			continue
		elif line[0] == 'Std:':
			std.append(str(line[1]))
			continue
		elif line[0] == 'Shortest:':
			shortest.append(str(line[1]))
			continue
		elif line[0] == 'Longest:':
			longest.append(str(line[1]))
			continue
		else:
			continue

with open(sys.argv[2], 'w') as stats:

	fastas = '\t'.join(fastas) + '\n'
	stats.write(fastas)
	genes = '\t'.join(genes) + '\n'
	stats.write(genes)
	residues = '\t'.join(residues) + '\n'
	stats.write(residues)
	medians = '\t'.join(medians) + '\n'
	stats.write(medians)
	q1 = '\t'.join(q1) + '\n'
	stats.write(q1)
	q3 = '\t'.join(q3) + '\n'
	stats.write(q3)
	iqr = '\t'.join(iqr) + '\n'
	stats.write(iqr)
	means = '\t'.join(means) + '\n'
	stats.write(means)
	std = '\t'.join(std) + '\n'
	stats.write(std)
	shortest = '\t'.join(shortest) + '\n'
	stats.write(shortest)
	longest = '\t'.join(longest) + '\n'
	stats.write(longest)
