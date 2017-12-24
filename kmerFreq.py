#!/usr/bin/python
'''USAGE: kmerFreq.py fasta kmer_size abundances.tsv
Counts kmer frequencies of a given size in a nucleotide genome fasta
'''
import sys


# Counts tetranucleotide frequency for all 4 frames in a single nucleotide string
def countKmers(contig, kmerDict, kmerSet, window):

	contig = contig.upper()

	for frame in range(0, window - 1, 1):

		kmerList = [contig[nucleotide:nucleotide + window] for nucleotide in range(frame, len(contig), window)]

		for kmer in kmerList:
			if len(kmer) < window or 'N' in kmer:
				continue

			try:
				kmerDict[kmer] += 1
				continue
			except KeyError:
				kmerDict[kmer] = 1
				kmerSet.add(kmer)

		# Normalize abundances by contig length
		for index in kmerSet:
			try:
				kmerDict[index] = kmerDict[index] / len(contig)
			except KeyError:
				continue

	return(kmerDict, kmerSet)


# Builds table of kmer abundances for each contig
def kmerTable(kmerDict, kmerSet, outFile):

	entry = [kmerDict['contig_name'], '\t']
	for kmer in kmerSet:
		try:
			entry.append(str(kmerDict[kmer]))
			entry.append('\t')
		except KeyError:
			continue

	entry = ''.join(entry) + '\n'
	outFile.write(entry)


# Read through and format nucleotide fasta, counting tetranucleotides along the way
with open(sys.argv[1], 'r') as inFasta:

	sequence = ''
	uniqueKmers = set()
	allDict = []
	windowSize = int(sys.argv[2])

	# Read in fist line
	firstLine = '\n'
	while firstLine == '\n':
		firstLine = inFasta.readline()
	kmerFreqDict = {}
	contig_name = firstLine.strip().lstrip('>').replace(' ', '_')
	kmerFreqDict['contig_name'] = contig_name

	for line in inFasta:
		if line[0] == '>':
			kmerFreqDict, uniqueKmers = countKmers(sequence, kmerFreqDict, uniqueKmers, windowSize)
			allDict.append(kmerFreqDict)
			sequence = ''
			kmerFreqDict = {}
			contig_name = firstLine.strip().lstrip('>').replace(' ', '_')
			kmerFreqDict['contig_name'] = contig_name
			continue
		else:
			sequence += line.strip()

kmerFreqDict, uniqueKmers = countKmers(sequence, kmerFreqDict, uniqueKmers, windowSize)
allDict.append(kmerFreqDict)


# Write final counts to a file
with open(sys.argv[3], 'w') as abundanceTable:
	entry = 'Contig\t' + '\t'.join(list(uniqueKmers)) + '\n'
	abundanceTable.write(entry)
	for contig in allDict:
		kmerTable(contig, uniqueKmers, abundanceTable)

