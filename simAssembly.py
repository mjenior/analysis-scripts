#!/usr/bin/env python
# Simulates assembled contigs using full genome refereces
# simAssembly.py genome.fasta 1500 10000

import sys
import os
import random 

def addGaps(sequence):

	leading = random.randint(1, 25)
	sequence = sequence[leading:]

	lagging = random.randint(1, 25)
	sequence = sequence[:-lagging] + '\n\n'

	return(sequence)

def pickLength(minimum, maximum):

	interval = int(round((maximum - minimum) / 10))
	prob = random.choice(range(0,100))

	d1 = range((9*interval), maximum)
	d2 = range((7*interval), (8*interval))
	d3 = range((6*interval), (7*interval))
	d4 = range((5*interval), (6*interval))
	d5 = range((4*interval), (5*interval))
	d6 = range((3*interval), (4*interval))
	d7 = range((2*interval), (3*interval))
	d8 = range(interval, (2*interval))
	d9 = range(minimum, interval)

	if prob >= 99: # 1%
		select_len = random.choice(d1)
	elif 99 > prob and prob >= 97: # 2%
		select_len = random.choice(d2)
	elif 97 > prob and prob >= 94: # 3%
		select_len = random.choice(d3)
	elif 94 > prob and prob >= 90: # 4%
		select_len = random.choice(d4)
	elif 90 > prob and prob >= 84: # 6%
		select_len = random.choice(d5)
	elif 84 > prob and prob >= 74: # 10%
		select_len = random.choice(d6)
	elif 74 > prob and prob >= 59: # 15%
		select_len = random.choice(d7)
	elif 59 > prob and prob >= 39: # 20%
		select_len = random.choice(d8)
	else: # 38%
		select_len = random.choice(d9)

	return(select_len)


def calcStats(lengths):

        total_seq = len(lengths) # Total number of sequences
        total_Mb = sum(lengths)/1000000.00 # Total number of residues expressed in Megabases
        total_Mb = "%.2f" % total_Mb

        lengths.sort()
        shortest = lengths[0]
        longest = lengths[-1]

        mid_pos = int(round(total_seq/2))
        median_len = lengths[mid_pos]
        q1 = lengths[0:mid_pos][int(len(lengths[0:mid_pos])/2)]
        q3 = lengths[mid_pos:-1][int(len(lengths[mid_pos:-1])/2)]

        #n50 calculation loop
        current_bases = 0
        n50 = 0
        n90 = 0
        seqs_1k = 0
        seqs_5k = 0
        seqs_10k = 0
        percent50_bases = int(round(sum(lengths)*0.5))
        percent90_bases = int(round(sum(lengths)*0.1))

        for index in lengths:
        	current_bases += index
        	if index > 1000:
        		seqs_1k += 1
        		if index > 5000:
        			seqs_5k += 1
        			if index > 10000:
        				seqs_10k += 1

        	if current_bases >= percent50_bases and n50 == 0:
        		n50 = index
        		l50 = lengths.count(index)
        	if current_bases >= percent90_bases and n90 == 0:
        		n90 = index

        return(total_seq, total_Mb, n50, n90, median_len, q1, q3, seqs_1k, seqs_5k, seqs_10k, shortest, longest)


#-------------------------------------------------------------------#


output_name = str(sys.argv[1]).rstrip('fastn') + 'simContigs.fasta'
output_file = open(output_name, 'w')
file_identifier = str(sys.argv[1]).split('.')[0]

min_len = int(sys.argv[2])
max_len = int(sys.argv[3])

with open(sys.argv[1], 'r') as genome_fasta:

	current_contig = 0
	current_seq = ''
	current_len = pickLength(min_len, max_len)
	seq_lengths = []
	bases_lost = 0

	for line in genome_fasta:

		if line == '\n':
			continue
		elif line[0] == '>':
			continue

		current_seq += line.strip()

		if len(current_seq) >= current_len:
			current_contig += 1
			current_contig_name = '>' + file_identifier + '_simContig_' + str(current_contig) + '\n'
			output_file.write(current_contig_name)

			output_seq = current_seq[:current_len] + '\n\n'
			#output_seq = addGaps(output_seq)
			output_file.write(output_seq)
			seq_lengths.append(len(output_seq)-4)
			current_seq = current_seq[current_len:]
			current_len = pickLength(min_len, max_len) # reassign new length

current_len = pickLength(min_len, max_len)
while len(current_seq) > current_len:
	current_contig += 1
	current_contig_name = '>' + file_identifier + '_simContig_' + str(current_contig) + '\n'
	output_file.write(current_contig_name)

	output_seq = current_seq[:current_len] + '\n\n'
	output_file.write(current_seq)
	seq_lengths.append(len(output_seq)-4)

	current_seq = current_seq[current_len:]
	current_len = pickLength(min_len, max_len)

current_contig += 1
current_contig_name = '>' + file_identifier + '_simContig_' + str(current_contig) + '\n'
output_file.write(current_contig_name)
output_seq = current_seq + '\n'
output_file.write(output_seq)
seq_lengths.append(len(output_seq)-2)
output_file.close()


stat_list = calcStats(seq_lengths)

output_string = """
# Simulated assembly: {fasta}
# Total contigs: {total_seq}
# Total bases: {total_mb} Mb
# N50: {n50}
# N90: {n90}
# Median length: {med_len}
# Q1: {q1}
# Q3: {q3}
# Contigs > 1 kb: {seqs_1k}
# Contigs > 5 kb: {seqs_5k}
# Contigs > 10 kb: {seqs_10k}
# Shorest contig: {shortest}
# Longest contig: {longest}
""".format(fasta = file_identifier,
	total_seq = str(stat_list[0]), 
	total_mb = str(stat_list[1]),
	n50 = str(stat_list[2]),
	n90 = str(stat_list[3]),
	med_len = str(stat_list[4]),
	q1 = str(stat_list[5]),
	q3 = str(stat_list[6]),
	seqs_1k = str(stat_list[7]),
	seqs_5k = str(stat_list[8]),
	seqs_10k = str(stat_list[9]),
	shortest = str(stat_list[10]),
	longest = str(stat_list[11]))

print output_string

