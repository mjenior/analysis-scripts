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
parser.add_argument('--bins', default='bins/', help='Directory for metagenomic contig bins')
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
total_include = 0
total_exclude = 0
countsDict = {}
print('\nOutlier contigs pruned:')
for index in bin_list:
	bin_name = index + fasta_ext
	new_bin_name = index + '.pruned.fna'
	new_bin = open(new_bin_name, 'w')
	in_count = 0
	out_count = 0
	with open(bin_name, 'r') as fasta:

		excluding = 0
		exclude = outlier_dict[index]
		for line in fasta:
			if line[0] == '>':
				in_count += 1
				seq_name = line.strip().replace('>','')
				if not seq_name in exclude:
					out_count += 1
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
	in_count = '(' + str(in_count) + ')'
	out_count = '(' + str(out_count) + ')'
	print(bin_name, in_count, '-->', new_bin_name, out_count)

# Report a few stats to the user
print('\nContigs excluded: ' + str(total_exclude))
print('Contigs included: ' + str(total_include))
perc_exclude = (float(total_exclude) / float(total_include)) * 100.0
perc_exclude = round(perc_exclude, 3)
print('Percent exclusion: ' + str(perc_exclude) + '%\n')

# Simply rename a copy of those fastas without outliers for continuity
print('\nNo outlier contigs detected:')
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
		print(src, '-->', dst)

print('')
if curr_wd != bin_dir:
	os.chdir(curr_wd)
