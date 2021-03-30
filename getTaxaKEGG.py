#!/usr/bin/python

import os
import sys
import pickle

script_path = str(os.path.dirname(os.path.realpath(__file__)))
prokaryotes = pickle.load(open(script_path + '/prokaryotes.pickle', 'rb'))

taxa = []
with open(sys.argv[1], 'r') as blastHits:
	for line in blastHits:
		taxon = line.split()[1]
		taxon = taxon.split(':')[0]
		taxa.append(taxon)

majority = 'none'
counter = 0
for x in taxa:
	curr_frequency = taxa.count(x)
	if(curr_frequency > counter):
		counter = curr_frequency
		majority = x 

try:
	trans_maj = prokaryotes[majority]
except KeyError:
	trans_maj = majority

perc = '(' + str(round((float(taxa.count(majority)) / float(len(taxa))) * 100.0, 1)) + '%)'
print(sys.argv[1], '|', trans_maj, '|', taxa.count(majority), 'of', len(taxa), perc)
