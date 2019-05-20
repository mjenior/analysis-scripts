#!/usr/bin/python3
'''USAGE: simReads.py contig_fasta read_length depth
Simulates short read sequencing efforts for a given fasta file, most likely assembled contigs.
'''
import sys
import math
import random
import argparse

# User defined arguments
parser = argparse.ArgumentParser(description='Generate a simulatated sequencing effort for a given fasta file.')
parser.add_argument('input_file')
parser.add_argument('--type', default='p', help='Denotes paired or single ends sequencing (default is p = paired, alternative is s = single)')
parser.add_argument('--read_len', default=250, help='Length or simulated output reads (default is 250bp)')
parser.add_argument('--coverage', default=1000, help='Depth of coverage for simulation (default is 1000X)')
parser.add_argument('--fragment', default=500, help='Simulated fragment length (default is 500bp)')
args = parser.parse_args()
input_fasta = str(args.input_file)
read_type = str(args.type)
read_len = int(args.read_len)
coverage = int(args.coverage)
fragment = int(args.fragment) + 15

# Generate output fasta file(s)
reads_f = input_fasta.split('/')[-1].rstrip('fastn') + str(read_len) + 'bp.R1.' + str(coverage) + 'X.sim_reads.fasta'
reads_f = open(reads_f, 'w')
if read_type != 's':
	reads_r = input_fasta.split('/')[-1].rstrip('fastn') + str(read_len) + 'bp.R2.' + str(coverage) + 'X.sim_reads.fasta'
	reads_r = open(reads_r, 'w')
	base_pairing = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

# Calculate depth needed
with open(input_fasta, 'r') as fasta:
	genome_size = 0
	for line in fasta:
		if line[0] == '>' or line == '\n':
			genome_size += len(line.strip())
read_total = (coverage * genome_size) / read_len
fragment_total = genome_size / fragment
depth = round(read_total / fragment_total)

# Identify longest sequence to correct coverage value
with open(input_fasta, 'r') as fasta:
        read_num = 0
        current_seq = ''
        for line in fasta:
        	if line[0] == '>' or line == '\n':
        		if current_seq == '':
        			continue
        		else:
        			# Generate sequence fragmentation
        			fragments = [current_seq[0+i:fragment+i] for i in range(0, len(current_seq), fragment)]
        			leading_positions = random.choices(range(1, 25), k=depth)
        			if read_type != 's':
        				lagging_positions = [-x for x in leading_positions]
        				random.shuffle(lagging_positions)

        			# Generate simulate reads
        			min_len = int(read_len - 25)
        			for seq in fragments:        				
        				# Cycle through randomly generated start sites
        				for x in range(0, len(leading_positions)):

        					# Remove a few bases from each side
        					lead_trim = random.randint(1,25)
        					lag_trim = random.randint(1,25) * -1
        					seq = seq[lead_trim:lag_trim]
        					if len(seq) < min_len: continue
        					seq = seq.upper()

        					# Single-end
        					read_num += 1
        					read_name = '>sim_read_F_' + str(read_num) + '\n'
        					start = leading_positions[x]
        					stop = start + read_len
        					read = seq[start:stop] + '\n'
        					reads_f.write(read_name)
        					reads_f.write(read)

        					# Paired-end
        					if read_type != 's':
        						read_name = '>sim_read_R_' + str(read_num) + '\n'
        						stop = lagging_positions[x]
        						start = start - read_len
        						read = seq[start:stop]

        						# Create reverse complement
        						read = list(read[::-1])
        						read = [base_pairing.get(base, base) for base in read]
        						read = ''.join(read) + '\n'
        						reads_r.write(read_name)
        						reads_r.write(read)

        			current_seq = ''
        			continue

        	else:
        		current_seq += line.strip()


# Close output files
reads_f.close()
if read_type == 'p':
	reads_r.close()

