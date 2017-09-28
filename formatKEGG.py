#!/usr/bin/env python
# USAGE: python formatKEGG.py
# Reformats genes.pep to be more bowtie-friendly and incorporates more of KEEG's annotation information

with open('ko_genes.list', 'r') as ko_genes:
	ko_dict = {}
	for line in ko_genes:
		line = line.strip().split()
		ko = line[0].split(':')[1]
		gene = line[1]
		ko_dict[gene] = ko

with open('pathway.list', 'r') as pathway:
	path_name_dict = {}
	for line in pathway:
		line = line.strip()
		if line[0] == '#':
			continue
		else:
			line = line.split()
			path = str(line[0])
			path_name = line[1]
			path_name_dict[path] = path_name

with open('ko.list', 'r') as ko_path:
	path_dict = {}
	for line in ko_path:
		line = line.split()
		path = line[0].split('ko')[1]
		path = path_name_dict[path]
		ko = line[1].split(':')[1]

		if not ko in path_dict.keys():
			path_dict[ko] = path
		else:
			path_dict[ko] = path_dict[ko] + ';' + path


with open('genes.pep', 'r') as kegg:

	out_file = open('kegg.aa.annotated.fasta', 'w')
	prev_pep = ''

	for line in kegg:

		if line == '\n':
			continue

		elif line[0] == '>':	
			line = line.split('  ')

			org = line[0].lstrip('>')
			try:
				ko = ko_dict[org]
			except KeyError:
				ko = 'no_ko_id'
			try:
				pathway = path_dict[ko]
			except KeyError:
				pathway = 'no_pathway_id'

			annotation = line[1].strip().split(';')
			if len(annotation) > 1:
				symbols = str(annotation[0]).replace(', ', '_')
				gene = annotation[1].strip().replace(',', '').replace(' ', '_')
			else:
				symbols = 'no_gene_symbols'
				gene = str(annotation[0]).replace(',', '').replace(' ', '_')

			prev_pep = prev_pep + '\n'
			out_file.write(prev_pep)
			prev_pep = ''
			entry = '>' + org + '|' + symbols + '|' + gene + '|' + ko + '|' + pathway + '\n'
			out_file.write(entry)

		else:
			prev_pep = prev_pep + line.strip()


out_file.write(prev_pep)
out_file.close()

