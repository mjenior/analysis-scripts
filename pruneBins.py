#!/usr/bin/python
'''USAGE: pruneBins.py outlier_table --ext fasta --bins bin_directory/
Checks quality of genome bins and collects most useable OGUs
'''
import sys
import argparse
import glob
import os
from shutil import copyfile

# User defined arguments
parser = argparse.ArgumentParser(description='Prune contig bins based on quality data')
parser.add_argument('outlier_table')
parser.add_argument('--ext', default='fa', help='Bin fasta file extension')
parser.add_argument('--bins', default='./', help='Directory for metagenomic contig bins')
parser.add_argument('--report', default='report.txt', help='Output text file with pruning report')

args = parser.parse_args()

# Assign variables
fasta_ext = '.' + str(args.ext)
curr_wd = str(os.getcwd())
if str(args.bins) == './':
	bin_dir = curr_wd
else:
	bin_dir = curr_wd + '/' + str(args.bins)
	os.chdir(bin_dir)

# Create dictionary of bin names with contig outliers in each
outlier_dict = {}
bin_list = []
with open(str(args.outlier_table), 'r') as outliers:
	for line in outliers:
		if line[0:6] == 'Bin Id' or line == '\n':
			continue
		contig_bin = line.split()[0]
		contig = line.split()[1]
		if not contig_bin in outlier_dict.keys():
			outlier_dict[contig_bin] = [contig]
			bin_list.append(contig_bin)
		else:
			outlier_dict[contig_bin].append(contig)


# Read bin fasta with outliers and write them to new files, omitting outliers
total_include_contigs = 0
total_exclude_contigs = 0
total_include_bases = 0
total_exclude_bases = 0
newFiles = []
for index in bin_list:
	bin_name = index + fasta_ext
	new_bin_name = index + '.pruned.fna'
	new_bin = open(new_bin_name, 'w')
	in_contigs = 0
	out_contigs = 0
	include_bases = 0
	exclude_bases = 0

	with open(bin_name, 'r') as fasta:

		excluding = 0
		exclude = outlier_dict[index]
		for line in fasta:
			if line[0] == '>':
				in_contigs += 1
				seq_name = line.strip().replace('>','')
				if not seq_name in exclude:
					out_contigs += 1
					excluding = 0
					total_include_contigs += 1
					new_bin.write(line)
					continue
				elif seq_name in exclude:
					excluding = 1
					total_exclude_contigs += 1
					continue
			elif excluding == 0:
				total_include_bases += len(line.strip())
				include_bases += len(line.strip())
				new_bin.write(line)
				continue
			else:
				total_exclude_bases += len(line.strip())
				exclude_bases += len(line.strip())

	new_bin.close()
	outStr = bin_name + ' (' + str(in_contigs) + ' contigs) --> ' + new_bin_name + ' (' + str(out_contigs) + ' contigs)\n'
	newFiles.append(outStr)


# Open report doc
reportFile = open(str(args.report), 'w')

# Report a few stats to the user
reportFile.write('Contigs excluded: ' + str(total_exclude_contigs) + '\n')
reportFile.write('Contigs included: ' + str(total_include_contigs) + '\n')
perc_exclude_contigs = (float(total_exclude_contigs) / float(total_include_contigs)) * 100.0
perc_exclude_contigs = round(perc_exclude_contigs, 3)
reportFile.write('Percent contig exclusion: ' + str(perc_exclude_contigs) + '%\n')

reportFile.write('\nBases excluded: ' + str(total_exclude_bases) + '\n')
reportFile.write('Bases included: ' + str(total_include_bases) + '\n')
perc_exclude_bases = (float(total_exclude_bases) / float(total_include_bases)) * 100.0
perc_exclude_bases = round(perc_exclude_bases, 3)
reportFile.write('Percent base exclusion: ' + str(perc_exclude_bases) + '%\n\n')

# Write files names and size changes to report
reportFile.write('Outlier contigs pruned from:\n')
for x in newFiles: reportFile.write(x)

# Simply rename a copy of those fastas without outliers for continuity
reportFile.write('\nNo outlier contigs detected in:\n')
fastas = '*' + fasta_ext
fastas = glob.glob(fastas)
unchanged = []
for current in fastas:
	current = current.replace(fasta_ext, '')
	current = current.replace('.pruned.fna', '')
	if not current in bin_list:
		src = current + fasta_ext
		dst = current + '.pruned.fna'
		copyfile(src, dst)
		reportFile.write(src + ' --> ' + dst + '\n')

reportFile.close()
if curr_wd != bin_dir:
	os.chdir(curr_wd)
