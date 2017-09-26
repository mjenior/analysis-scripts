#!/usr/bin/python
'''USAGE: sliceFastx.py reads.fasta reads_per_slice
Slices a large fasta or fastq file into a series of files with a user defined number of reads
'''
import sys


def sliceFastq(fastq, seq_lmt, sample_name):

	curr_seq = 0
	curr_slice = 1
	curr_out = sample_name + '.slice_' + str(curr_slice) + '.fastq'
	curr_out = open(curr_out, 'w')

	for line in fastq:

		if curr_seq == seq_lmt:
			curr_out.close()
			curr_slice += 1
			curr_out = sample_name + '.slice_' + str(curr_slice) + '.fastq'
			curr_out = open(curr_out, 'w')
			curr_seq = 0

		if line[0] == '@':
			curr_seq += 1
		
		curr_out.write(line)

	curr_out.close()
	return(curr_slice)


def sliceFasta(fasta, seq_lmt, sample_name):

	curr_seq = 0
	curr_slice = 1
	curr_out = sample_name + '.slice_' + str(curr_slice) + '.fasta'
	curr_out = open(curr_out, 'w')

	for line in fasta:

		if curr_seq == seq_lmt:
			curr_out.close()
			curr_slice += 1
			curr_out = sample_name + '.slice_' + str(curr_slice) + '.fasta'
			curr_out = open(curr_out, 'w')
			curr_seq = 0

		if line[0] == '>':
			curr_seq += 1
		
		curr_out.write(line)

	curr_out.close()
	return(curr_slice)


# Set slice size
slice_size = int(sys.argv[2])
sample = str(sys.argv[1]).split('/')[-1]
sample = str(sample).split('.')[0]

with open(sys.argv[1], 'r') as input_file:
	if str(sys.argv[1])[-1] == 'q':
		slices = sliceFastq(input_file, slice_size, sample)
	else:
		slices = sliceFasta(input_file, slice_size, sample)


print('Total slices: ' + str(slices))

