#!/usr/bin/python
'''USAGE: simReads.py contig_fasta read_length depth
Simulates short read sequencing efforts for a given fasta file, most likely assembled contigs.
'''
import sys
import math
import random
import argparse

# Define variables
parser = argparse.ArgumentParser(description='Generate bipartite metabolic models and calculates importance of substrate nodes based on gene expression.')
parser.add_argument('fasta')
parser.add_argument('--len', default=250, help='Length of reads to be simullated')
parser.add_argument('--cov', default=500, help='Average depth of sequencing per contig')
parser.add_argument('--pair', default=False, help='Defines if you want paired-end of single ends simulated reads')
args = parser.parse_args()

# Assign variables
fasta = str(args.fasta)
read_len = int(args.len)
coverage = int(args.cov)
paired = args.pair

# Generate output fasta file
if paired == True: pair_lab = 'paired'
else: pair_lab = 'single'
output_fasta = str(sys.argv[1]).split('/')[-1].split('.fasta')[0] + '.' + str(read_len) + 'bp.' + str(coverage) + 'X.' + pair_lab + '.simreads.fasta'

# Identify longest sequence to correct coverage value
with open(sys.argv[1], 'r') as fasta:
        max_len = 0
        for line in fasta:
                if line[0] == '>' or line == '\n':
                        continue
                elif len(line.strip()) > max_len:
                        max_len = len(line.strip())

# Calculate necessary depth to acheive desired coverage
depth = (max_len * coverage) / read_len

# Generate simulated reads
reads = open(output_fasta, 'w')
with open(sys.argv[1], 'r') as contigs:

        read_count = 1
        for line in contigs:
                if line[0] == '>' or line == '\n': continue

                curr_seq = line.strip()
                curr_len = len(curr_seq) - read_len
                curr_depth = round((float(len(curr_seq)) / max_len) * depth)

                for index in range(0,int(curr_depth)):
                        curr_name = '>sim_read_' + str(read_count) + '\n'
                        reads.write(curr_name)
                        read_count += 1

                        curr_start = random.randint(0,curr_len)
                        curr_end = curr_start + read_len
                        curr_read = curr_seq[curr_start:curr_end] + '\n'
                        reads.write(curr_read)

reads.close()

