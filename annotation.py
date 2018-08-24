#!/usr/bin/python
'''USAGE: fixAnnotation.py fixed_mapping_file
Adds inproved gene and taxonomy annotation to idx files. Also pools duplicate gene entries.
'''
import sys


with open('kegg_organisms.tsv', 'r') as kegg:

	kegg_dict = {}
	for line in kegg:
		line = line.split()
		if not line[0] == 'kegg_code':
			kegg_dict[line[0]] = line[2]
		else:
			continue
print('Done reading in KEGG.')

with open('hmp2_metatranscriptomes.tsv','r') as annotation:

	idx_dict = {}
	annotation_set = set()
	current = 1
	for line in annotation:
		current += 1
		if current % 1000 == 0: print(current)
		line = line.split()
		if line[0] == 'gene':
			continue
		elif line[0][0:4] == 'k93_':
			continue
			
		annotation = line[0].split('|')
		del annotation[-1]
		org = annotation[0].split(':')[0]
		species = kegg_dict[org]
		annotation.append(species)
		genus = species.split('_')[0]
		annotation.append(genus)
		annotation = '\t'.join(annotation)

		try:
			idx_dict[annotation][0] = idx_dict[annotation][0] + float(line[1])
			idx_dict[annotation][2] = idx_dict[annotation][3] + float(line[4])
			idx_dict[annotation][4] = idx_dict[annotation][4] + float(line[5])
		except KeyError:
			idx_dict[annotation] = [float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6])]
	
print('Done reading in mapping file.')

with open(sys.argv[1], 'w') as outfile:

	outfile.write('kegg_gene\tgene_symbol\tgene_name\tko\tkegg_pathway\tevalue\ttaxon\tgenera\tCD_metaG\tCD_norm\tUC_metaG\tUC_norm\tnonIBD_metaG\tnonIBD_norm\n')

	for index in idx_dict.keys():
		mapping = '\t'.join([str(x) for x in idx_dict[index]])
		entry = index + '\t' + mapping + '\n'
		outfile.write(entry)

print('Done writing to new file.')
