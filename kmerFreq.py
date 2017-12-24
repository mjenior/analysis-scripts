#!/usr/bin/python
'''USAGE: kmerFreq.py fasta kmer_size > abundances.txt
Counts kmer frequencies of a given size in a nucleotide genome fasta
'''
import sys


# Counts tetranucleotide frequency for all 4 frames in a single nucleotide string
def countKmers(contig, kmerDict, kmerSet, window):

	contig = contig.upper()

	for frame in range(0:window - 1):

		kmerList = [contig[nucleotide:nucleotide + window] for nucleotide in range(frame, len(contig), window)]

		for kmer in kmerList:
			if len(kmer) < window or 'N' in kmer:
				continue

			if not kmer in kmerSet:
				kmerDict[kmer] = 1
				kmerSet.add(kmer)
				continue
			else:
				kmerDict[kmer] += 1

	return(kmerDict, kmerSet)


# Read through and format nucleotide fasta, counting tetranucleotides along the way
with open(sys.argv[1], 'r') as inFasta:

	seq = ''
	kmerFreqDict = {}
	uniqueKmers = set()
	windowSize = int(sys.argv[2])

	for line in inFasta:
		if line[0] == '>':
			kmerFreqDict, uniqueKmers = countKmers(seq, kmerFreqDict, uniqueKmers, windowSize)
			seq = ''
			continue
		else:
			seq += line.strip()

kmerFreqDict, uniqueKmers = countKmers(seq, kmerFreqDict, uniqueKmers, windowSize)


# Print results
for kmer in uniqueKmers:
	print(kmer + '\t' + str(kmerFreqDict[kmer]))


