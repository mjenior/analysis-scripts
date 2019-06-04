#!/usr/bin/env python
# Simulates assembled contigs using a full genome reference

import sys
import os
import random 
import argparse

# User defined arguments
parser = argparse.ArgumentParser(description='Generate simulated assembled contigs for a genome fasta.')
parser.add_argument('genome_file')
parser.add_argument('--min', default=1500, help='Minimum length of simulated output contigs (default is 1500 bp)')
parser.add_argument('--max', default=35000, help='Maximum length of simulated output contigs (default is 35000 bp)')
args = parser.parse_args()
genome_file = str(args.genome_file)
min_len = int(args.min)
max_len = int(args.max)

# Create output fasta file name
contigs_file = genome_file.rstrip('fastn') + str(min_len) + 'bp.' + str(max_len) + 'bp.' + 'sim_contigs.fasta'

#-------------------------------------------------------------------#

# Trims a small amount of reads off both ends of a contig
def addContigGaps(sequence):

	leading = random.randint(1, 20)
	lagging = random.randint(1, 20)
	sequence = sequence[leading:-lagging] + '\n'

	return(sequence)

# Select a contig length based on a discrete probability distribution
def pickContigLength(minimum = 1500, maximum = 90000):

	interval = int(round((maximum - minimum) / 10))
	prob = random.choice(range(0,100))

	d1 = range((9 * interval), maximum)
	d2 = range((7 * interval), (8 * interval))
	d3 = range((6 * interval), (7 * interval))
	d4 = range((5 * interval), (6 * interval))
	d5 = range((4 * interval), (5 * interval))
	d6 = range((3 * interval), (4 * interval))
	d7 = range((2 * interval), (3 * interval))
	d8 = range(interval, (2 * interval))
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
	else: # 38% and below
		select_len = random.choice(d9)

	return(select_len)

#-------------------------------------------------------------------#

# Create the simulated assembly and read data
contigs_file = open(contigs_file, 'w')
with open(genome_file, 'r') as genome_fasta:

	contig_count = 0
	current_seq = ''
	current_len = pickContigLength(min_len, max_len)

	for line in genome_fasta:
		if line == '\n' or line[0] == '>': continue
		
		current_seq += line.strip()
		while len(current_seq) > current_len:
			contig_count += 1

			current_contig_name = '>sim_contig_' + str(contig_count) + '\n'
			contigs_file.write(current_contig_name)

			output_seq = current_seq[:current_len]
			output_seq = addContigGaps(output_seq) # Introduce artificial gaps in the assembly
			contigs_file.write(output_seq)

			current_seq = current_seq[current_len:]
			current_len = pickContigLength(min_len, max_len)

		if len(current_seq) > min_len:
			contig_count += 1

			current_contig_name = '>sim_contig_' + str(contig_count) + '\n'
			contigs_file.write(current_contig_name)

			output_seq = current_seq[:current_len]
			output_seq = addContigGaps(output_seq) # Introduce artificial gaps in the assembly
			contigs_file.write(output_seq)


# Close output file
contigs_file.close()
