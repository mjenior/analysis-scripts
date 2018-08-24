#!/usr/bin/env python
# USAGE: splitFastq.py interleaved_fastq
# Splits an interleaved fastq into separate files of forward and reverse reads

import sys

read_1 = str(sys.argv[1]).rstrip('fastq') + 'R1.fastq'
read_1 = open(read_1, 'w')
read_2 = str(sys.argv[1]).rstrip('fastq') + 'R2.fastq'
read_2 = open(read_2, 'w')


with open(sys.argv[1], 'r') as fastq:

	current_read = 0

	for line in fastq:

		if line[0] == '@' and line.strip()[-1] == '1':
			line = line.replace(' ', '_')
			current_read = 1
			read_1.write(line)
			continue
		elif line[0] == '@' and line.strip()[-1] == '2':
			line = line.replace(' ', '_')
			current_read = 2
			read_2.write(line)
			continue

		if current_read == 1:
			read_1.write(line)
			continue
		elif current_read == 2:
			read_2.write(line)


read_1.close()
read_2.close()


