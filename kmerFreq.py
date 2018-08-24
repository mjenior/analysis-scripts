#!/usr/bin/python
'''USAGE: kmerFreq.py fasta kmer_size
Counts kmer frequencies of a given size in a nucleotide genome fasta
'''
import sys
import itertools

# Counts tetranucleotide frequency for all 4 frames in a single nucleotide string
def countKmers(contig, kmerDict, window):

	contig = contig.upper()
	numKmers = ((len(contig) - window)) + 1
	kmerDict['kmer_sum'] = numKmers

	for i in range(0, numKmers, 1):
		kmer = contig[i:i + window]

		if len(kmer) < window or 'N' in kmer:
			continue
		try:
			kmerDict[kmer] += 1
			continue
		except KeyError:
			kmerDict[kmer] = 1

	return(kmerDict)


# Builds table of kmer abundances for each contig
def kmerTable(kmerSet, kmerDict, outFile):

	entry = [kmerDict['contig_name']]
	for kmer in kmerSet:
		try:
			entry.append(str( kmerDict[kmer] / kmerDict['kmer_sum'] ))
		except KeyError:
			entry.append('0')
			continue
	
	entry = '\t'.join(entry) + '\n'
	outFile.write(entry)


# Read through and format nucleotide fasta, counting tetranucleotides along the way
outFile = str(sys.argv[1]).split('.')[0] + '.' + str(sys.argv[2]) + 'mer.frequency.tsv'
print('Writing kmer abundances to ' + outFile)
outFile = open(outFile, 'w')

with open(sys.argv[1], 'r') as inFasta:

	windowSize = int(sys.argv[2])
	uniqueKmers = set([''.join(x) for x in itertools.product(['A','T','G','C'], repeat = windowSize)])

	entry = '\t'.join(['Contig'] + list(uniqueKmers)) + '\n'
	outFile.write(entry)

	# Read in fist line
	firstLine = '\n'
	while firstLine == '\n': firstLine = inFasta.readline()
	contig_name = firstLine.strip().lstrip('>').replace(' ', '_')
	kmerFreqDict = {}
	kmerFreqDict['contig_name'] = contig_name
	sequence = []

	status = 1
	for line in inFasta:
		if line[0] == '>':
			sequence = ''.join(sequence)
			kmerFreqDict = countKmers(sequence, kmerFreqDict, windowSize)
			kmerTable(uniqueKmers, kmerFreqDict, outFile)

			sequence = []
			kmerFreqDict = {}
			contig_name = line.strip().lstrip('>').replace(' ', '_')
			kmerFreqDict['contig_name'] = contig_name
			
			status += 1
			if status % 500 == 0:
				print(status)
			continue
		else:
			sequence.append(line.strip())

sequence = ''.join(sequence)
kmerFreqDict = countKmers(sequence, kmerFreqDict, windowSize)
kmerTable(uniqueKmers, kmerFreqDict, outFile)
outFile.close()

