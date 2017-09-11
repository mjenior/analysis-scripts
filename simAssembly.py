#!/usr/bin/env python
# Simulates assembled contigs using full genome refereces
# simAssembly.py genome.fasta min_contig_length max_contig_length

import sys
import os
import random 

def addGaps(sequence):

	leading = random.randint(10, 100)
	sequence = sequence[leading:]

	lagging = random.randint(10, 100)
	sequence = sequence[:-lagging] + '\n\n'

	return(sequence)


def pickLength(minimum, maximum):

	fifth = int((maximum - minimum) / 5)

	high = range((4*fifth), maximum)
	high_mid = range((3*fifth), (4*fifth))
	mid = range((2*fifth), (3*fifth))
	low_mid = range(fifth, (2*fifth))
	low = range(minimum, fifth)

	prob = random.choice(range(0,100))

	if prob >= 97:
		select_len = random.choice(high)
	elif 97 > prob and prob >= 93:
		select_len = random.choice(high_mid)
	elif 93 > prob and prob >= 81:
		select_len = random.choice(mid)
	elif 81 > prob and prob >= 60:
		select_len = random.choice(low_mid)
	else:
		select_len = random.choice(low)

	return(select_len)


def calcStats(lengths):

        total_seq = len(lengths) # Total number of sequences
        total_Mb = sum(lengths)/1000000.00 # Total number of residues expressed in Megabases
        total_Mb = "%.2f" % total_Mb

        lengths.sort()
        shortest = lengths[0]
        longest = lengths[-1]
        median_len = lengths[int(round(total_seq/2))] 
        q1 = lengths[int(round(len(lengths) * 0.25))]
        q3 = lengths[int(round(len(lengths) * 0.75))]

        #n50 calculation loop
        current_bases = 0
        n50 = 0
        n90 = 0
        seqs_1k = 0
        seqs_5k = 0
        percent50_bases = int(round(sum(lengths)*0.5))
        percent90_bases = int(round(sum(lengths)*0.1))

        for index in lengths:
        	current_bases += index
        	if index > 1000:
        		seqs_1k += 1
        	if index > 5000:
        		seqs_5k += 1

        	if current_bases >= percent50_bases and n50 == 0:
        		n50 = index
        	if current_bases >= percent90_bases and n90 == 0:
        		n90 = index

        return(total_seq, total_Mb, n50, n90, median_len, q1, q3, seqs_1k, seqs_5k, shortest, longest)


#-------------------------------------------------------------------#


output_file = str(sys.argv[1]).rstrip('fastn') + 'sim_contigs.fasta'
output_file = open(output_file, 'w')

min_len = int(sys.argv[2]) + 200
max_len = int(sys.argv[3]) + 20

with open(sys.argv[1], 'r') as genome_fasta:

	current_contig = 1
	current_seq = ''
	current_len = pickLength(min_len, max_len)
	seq_lengths = []

	for line in genome_fasta:

		if line == '\n':
			continue
		elif line[0] == '>':
			continue

		current_seq += line.strip()

		if len(current_seq) >= current_len:

			current_contig_name = '>Simulated_contig_' + str(current_contig) + '\n'
			output_file.write(current_contig_name)
			current_contig += 1

			output_seq = current_seq[:current_len]
			output_seq = addGaps(output_seq)
			output_file.write(output_seq)
			seq_lengths.append(len(output_seq))

			current_seq = current_seq[current_len:]
			current_len = pickLength(min_len, max_len) # reassign new length


current_contig_name = '>Simulated_contig_' + str(current_contig) + '\n'
output_file.write(current_contig_name)
output_file.write(current_seq)
output_file.close()

stat_list = calcStats(seq_lengths)
output_string = """
# Total contigs: {total_seq}
# Total bases: {total_mb} Mb
# N50: {n50}
# N90: {n90}
# Median length: {med_len}
# Q1: {q1}
# Q3: {q3}
# Contigs > 1 kb: {seqs_1k}
# Contigs > 5 kb: {seqs_5k}
# Shorest contig: {shortest}
# Longest contig: {longest}
""".format(total_seq = str(stat_list[0]), 
	total_mb = str(stat_list[1]),
	n50 = str(stat_list[2]),
	n90 = str(stat_list[3]),
	med_len = str(stat_list[4]),
	q1 = str(stat_list[5]),
	q3 = str(stat_list[6]),
	seqs_1k = str(stat_list[7]),
	seqs_5k = str(stat_list[8]),
	shortest = str(stat_list[9]),
	longest = str(stat_list[10]))

print output_string

