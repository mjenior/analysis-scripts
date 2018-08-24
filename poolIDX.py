#!/usr/bin/python
'''USAGE: poolIDX.py files.txt output_file_name
Pools all IDX stats files listed in txt file
'''

import sys

def add2dict(idx, idx_dict):

	with open(idx, 'r') as current:

		for line in current:
			gene = str(line.split()[0])
			if gene == 'gene_target': continue
			reads = int(line.split()[1])

			if not gene in idx_dict.keys():
				idx_dict[gene] = reads
			else:
				idx_dict[gene] = idx_dict[gene] + reads

	return(idx_dict)


gene_dict = {}
with open(sys.argv[1], 'r') as files:
	for line in files:
		if line == '\n': continue
		gene_dict = add2dict(line.strip(), gene_dict)


with open(sys.argv[2], 'w') as out_file:
	header = 'gene\tnorm_read_abund\n'
	out_file.write(header)
	for index in gene_dict.keys():
		entry = index + '\t' + str(gene_dict[index]) + '\n'
		out_file.write(entry)

