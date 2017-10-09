#!/usr/bin/python
'''USAGE: collateIDX.py gene_list files.txt output_file_name
Combines all IDX stats files listed in txt file into a shared files of read mappings
'''

import sys


def add2dict(idx, idx_dict):

	with open(idx, 'r') as current:
		genes = idx_dict.keys()

		for line in current:
			gene = line.split()[0]
			reads = line.split()[1]
			try:
				genes.remove(gene)
			except ValueError:
				pass

			if gene == 'gene_target': continue

			if not gene in idx_dict.keys():
				idx_dict[gene] = [str(reads)]
			else:
				idx_dict[gene].append(str(reads))

		for index in genes:
			idx_dict[index].append('0')

	return(idx_dict)


gene_lst = []
with open(sys.argv[1], 'r') as genes:
	for line in genes:
		gene_lst.append(line.split()[0])
gene_lst = list(set(gene_lst))
idx_dictionary = {}
for index in gene_lst:
	idx_dictionary[index] = []


header = ['gene_target']
with open(sys.argv[2], 'r') as files:
	for line in files:
		samp = line.strip().split('.')[0]
		header.append(samp)
		idx_dictionary = add2dict(line.strip(), idx_dictionary)


with open(sys.argv[3], 'w') as out_file:
	header = '\t'.join(header) + '\n'
	out_file.write(header)
	for index in idx_dictionary.keys():
		entry = [index] + idx_dictionary[index]
		entry = '\t'.join(entry) + '\n'
		out_file.write(entry)



