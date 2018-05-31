#!/usr/bin/python
'''USAGE: pruneBins.py outlier_table
Checks quality of genome bins and collects most useable OGUs
'''
import sys
import os
import argparse
import gzip

# User defined arguments
parser = argparse.ArgumentParser(description='Generate bipartite metabolic models and calculates importance of substrate nodes based on gene expression.')
parser.add_argument('outlier_table')
parser.add_argument('--ext', default='fa', help='Bin fasta file extension')
parser.add_argument('--bins', default='bins/', help='Directory for metagenomic contig bins')
args = parser.parse_args()

# Assign variables
outliers = open(str(args.outlier_table), 'r')
fasta_ext = str(args.ext)
bin_dir = str(os.getcwd()) + '/' + str(args.bins)
os.chdir(bin_dir)

outlier_dict = {}
bin_list = []
for line in outliers:
	if line[0:6] == 'Bin Id':
		continue
	contig_bin = line.split()[0]
	contig = line.split()[1]
	if not contig_bin in outlier_dict.keys():
		outlier_dict[contig_bin] = [contig]
		bin_list.append(contig_bin)
	else:
		outlier_dict[contig_bin].append(contig)
outliers.close()

total_include = 0
total_exclude = 0

for index in bin_list:
	bin_name = index + '.' + fasta_ext
	new_bin_name = index + '.pruned.' + fasta_ext

	new_bin = open(new_bin_name, 'w')
	with open(bin_name, 'r') as fasta:

		excluding = 0
		exclude = outlier_dict[index]
		for line in fasta:
			if line[0] == '>':
				seq_name = line.strip().replace('>','')
				if not seq_name in exclude:
					excluding = 0
					total_include += 1
					new_bin.write(line)
					continue
				elif seq_name in exclude:
					excluding = 1
					total_exclude += 1
					continue
			elif excluding == 0:
				new_bin.write(line)

	new_bin.close()

print('Contigs excluded: ' + str(total_exclude))
print('Contigs included: ' + str(total_include))

perc_exclude = (float(total_exclude) / float(total_include)) * 100.0
perc_exclude = round(perc_exclude, 4)
print('Percent exclusion: ' + str(perc_exclude) + '%')


