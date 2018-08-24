#!/usr/bin/python
'''USAGE: tetraNucFreq.py fasta frequencies
This script calculates tetranucleotide frequencies
'''
import sys
import itertools

nucs = ['A','T','G','C']
tetras = []
for curr_tetras in itertools.combinations_with_replacement(nucs, 4):
	curr_tetras = list(itertools.permutations(list(curr_tetras)))
	for x in curr_tetras:
		tetras.append(''.join(list(x)))
tetras = list(set(tetras))

outfile = open(sys.argv[2], 'w')
entry = ['seq_name'] + tetras
entry = '\t'.join(entry) + '\n'
outfile.write(entry)

progress = 0
with open(sys.argv[1], 'r') as fasta:

	for line in fasta:
		if line == '\n':
			continue
		elif line[0] == '>':
			progress += 1
			if progress % 100 == 0:
				print(progress)
			entry = line.split()
			entry = '_'.join(entry).replace('>','') + '\t'
			outfile.write(entry)
			continue
		else:
			seq = map(''.join,zip(*[line.strip()[i:] for i in range(4)]))
			seq_len = float(len(seq))
			curr_freq = {x:0 for x in tetras}

			for tetra in seq:
				curr_freq[tetra] += 1

			index = 0
			for tetra in tetras:
				freq = str(float(curr_freq[tetra]) / seq_len)
				index += 1
				if index == len(tetras):
					index = 0
					freq = freq + '\n'
					outfile.write(freq)
				else:
					freq = freq + '\t'
					outfile.write(freq)

outfile.close()
