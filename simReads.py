#!/usr/bin/python3
'''USAGE: simReads.py contig_fasta read_length depth
Simulates short read sequencing efforts for a given fasta file, most likely assembled contigs.
'''
import sys
import numpy
import random
import argparse

# User defined arguments
parser = argparse.ArgumentParser(description='Generate a simulatated sequencing effort for a given fasta file.')
parser.add_argument('input_file')
parser.add_argument('--type', default='p', help='Denotes paired or single ends sequencing (default is p = paired, alternative is s = single)')
parser.add_argument('--read_len', default=150, help='Length or simulated output reads (default is 250bp)')
parser.add_argument('--coverage', default=50, help='Depth of coverage for simulation (default is 1000X)')
#  https://doi.org/10.1371/journal.pone.0104579
parser.add_argument('--fragment', default=300, help='Simulated fragment length (default is 500bp)')
# Mitochondrial DNA A DNA Mapp Seq Anal. 2018 Aug;29(6):840-845. doi: 10.1080/24701394.2017.1373106. Epub 2017 Sep 5.
args = parser.parse_args()
input_fasta = str(args.input_file)
read_type = str(args.type)
read_len = int(args.read_len)
coverage = int(args.coverage)
fragment = int(args.fragment)
fragment_dist = numpy.random.normal(fragment, 50, 1000)


# Generate random fragments and calculate depth needed per fragment
print('\rFragmenting genome...')
with open(input_fasta, 'r') as fasta:
	genome_size = 0
	current_seq = ''
	fragments = set()
	for line in fasta:
		if line[0] == '>' or line == '\n':
			if current_seq == '':
				continue
			else:
				for x in range(0, coverage):
					fragment = int(round(random.choice(fragment_dist)))
					leading = random.randint(0, fragment-1)
					fragments |= set([current_seq[0+i:fragment+i] for i in range(leading, len(current_seq), fragment)])
					current_seq == ''
					continue

		current_seq += line.strip().upper()
		genome_size += len(current_seq)

read_total = (coverage * genome_size) / read_len
fragment_total = len(fragments)
depth = round(read_total / fragment_total)


# Generate output fasta file(s)
reads_f = input_fasta.split('/')[-1].rstrip('fastn') + 'R1.' + str(read_len) + 'bp.' + str(coverage) + 'X.sim_reads.fasta'
reads_f = open(reads_f, 'w')
if read_type != 's':
	reads_r = input_fasta.split('/')[-1].rstrip('fastn') + 'R2.' + str(read_len) + 'bp.' + str(coverage) + 'X.sim_reads.fasta'
	reads_r = open(reads_r, 'w')
	base_pairing = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}


# Generate simulate reads
read_num = 0
increment = 100.0 / float(fragment_total)
progress = 0.0
sys.stdout.write('\rSimulating reads... ' + str(progress) + '%')
sys.stdout.flush() 
for seq in fragments:
	if len(seq) < read_len * 0.9: continue

	for x in range(0, depth):

		# Single-end - 5'
		read_num += 1
		read_name = '>sim_read_F_' + str(read_num) + '\n'
		read = seq[0:read_len] + '\n'
		reads_f.write(read_name)
		reads_f.write(read)

		# Paired-end - 3'
		if read_type != 's':
			read_name = '>sim_read_R_' + str(read_num) + '\n'
			read = seq[-read_len:]

			# Create reverse complement
			read = list(read[::-1])
			read = [base_pairing.get(base, base) for base in read]
			read = ''.join(read) + '\n'
			reads_r.write(read_name)
			reads_r.write(read)

	progress += increment
	progress = float("%.3f" % progress)
	sys.stdout.write('\rSimulating reads... ' + str(progress) + '%')
	sys.stdout.flush() 


# Close output files
reads_f.close()
if read_type != 's':
	reads_r.close()

