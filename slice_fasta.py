#!/usr/bin/python
'''USAGE: slice_fasta.py reads.fasta reads_per_slice
Slices a large fasta file into a series of files with a user defined number of reads
'''
import sys
import os

# Set slice size
slice_size = int(sys.argv[2])

# Create and navigate to new output directory
working_dir = str(os.getcwd())
output_dir = working_dir + '/sliced_size_' + str(slice_size)
if not os.path.exists(output_dir):	
	os.makedirs(output_dir)
os.chdir(output_dir)

# Read fasta, writing to new smaller files as you go
with open(sys.argv[1], 'r') as input_fasta:

	fasta_count = 1
	current_output_name = 'sliced_' + str(fasta_count) + '.fasta'
	current_output = open(current_output_name, 'w')
	empty = 1

	included = 0
	for line in input_fasta:
		
		if line[0] == '>':
			included += 1
			current_output.write(line)
			empty = 0
			continue
		else:
			current_output.write(line)
			empty = 0

		if included == slice_size:
			current_output.close()
			included = 0
			fasta_count += 1
			current_output_name = 'sliced_' + str(fasta_count) + '.fasta'
			current_output = open(current_output_name, 'w')
			empty = 1

current_output.close()
if empty != 0:
		os.remove(current_output_name)
		fasta_count -= 1


print(''.join(['Total Fasta slices: ', str(fasta_count)]))
os.chdir(working_dir)

