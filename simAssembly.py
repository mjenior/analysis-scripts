#!/usr/bin/env python
# Simulates assembled contigs and sequencing reads using full genome refereces
# simAssembly.py genome.fasta 

import sys
import os
import random 

# Trims a small amount of reads off both ends of a contig
def addContigGaps(sequence):

	leading = random.randint(1, 20)
	sequence = sequence[leading:]

	lagging = random.randint(1, 20)
	sequence = sequence[:-lagging]

	sequence = sequence + '\n\n'

	return(sequence)

# Select a contig length based on a discrete probability distribution
def pickContigLength():

	minimum = 250
	maximum = 50000

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

# Generate a single read in a random place within a contig
def generateRead(contig, read_len):
	last_avail = len(contig) - read_len - 1
	start_pos = random.choice(range(0, last_avail))
	end_pos = start_pos + read_len
	read = contig[start_pos:end_pos]
	read = read + '\n\n'
	return read

# Brings all functions together and does the work
def createSeqs(current_contig, current_seq, current_len, contigs_file, reads_file, read_count):

	seq_depth = 50
	read_length = 150

	current_contig += 1
	if current_contig % 10 == 0:
		print(current_contig)

	current_contig_name = '>SimContig_' + str(current_contig) + '\n'
	contigs_file.write(current_contig_name)

	output_seq = current_seq[:current_len]
	output_seq = addContigGaps(output_seq) # Introduce artificial gaps in the assembly
	contigs_file.write(output_seq)

	current_seq = current_seq[current_len:]

	num_reads = (seq_depth * len(output_seq)) / read_length
	num_reads = int(round(num_reads))

	for x in range(0, num_reads):
		read_count += 1
		current_read_name = '>SimRead_' + str(read_count) + '\n'
		reads_file.write(current_read_name)
		current_read = generateRead(output_seq, read_length)
		reads_file.write(current_read)

	return(current_seq, current_contig, read_count)

#-------------------------------------------------------------------#

# Create output contig and read files
fasta_name = str(sys.argv[1]).rstrip('fastn')
contigs_file = fasta_name + 'contigs.fasta'
print('\nWriting simulated contigs to ' + contigs_file)
contigs_file = open(contigs_file, 'w')

reads_file = fasta_name + 'reads.fasta'
print('Writing simulated reads to ' + reads_file + '\n')
reads_file = open(reads_file, 'w')

#-------------------------------------------------------------------#

# Create the simulated assembly and read data
with open(sys.argv[1], 'r') as genome_fasta:

	contig_number = 0
	read_number = 0
	current_seq = ''

	current_len = pickContigLength()
	for line in genome_fasta:

		if line == '\n' or line[0] == '>':
			continue

		current_seq += line.strip()
		if len(current_seq) >= current_len:
			current_seq, contig_number, read_number = createSeqs(contig_number, current_seq, current_len, contigs_file, reads_file, read_number)
			current_len = pickContigLength()

while len(current_seq) > current_len:
	current_seq, contig_number, read_number = createSeqs(contig_number, current_seq, current_len, contigs_file, reads_file, read_number)
	current_len = pickContigLength()

current_seq, contig_number, read_number = createSeqs(contig_number, current_seq, current_len, contigs_file, reads_file, read_number)

#-------------------------------------------------------------------#

# Close output files
print('')
contigs_file.close()
reads_file.close()

