#!/usr/bin/python
'''USAGE: readBLAST.py blast.out
Reformats BLAST output to be parsed later
'''
import sys

out_file = str(sys.argv[1]).rstrip('out') + 'format.txt'
print('Output file: ' + out_file)
out_file = open(out_file, 'w')
out_file.write('query\tkegg_org_hit\tgene_hit\tpercent_id\te_vlaue\n')

with open(sys.argv[1], 'r') as in_file:

	for line in in_file:
		if line == '\n': continue

		query = line.split()[0].split('_')[0]
		hit = line.split()[1].split('|')
		org = hit[0].split(':')[0]
		if len(hit) == 3:
			hit = hit[1]
		else:
			hit = hit[1] + '|' + hit[2]
		perc_id = str(line.split()[2])
		evalue = str(line.split()[10])

		entry = query + '\t' + org + '\t' + hit + '\t' + perc_id + '\t' + evalue + '\t' + '\n'
		out_file.write(entry)


out_file.close()

