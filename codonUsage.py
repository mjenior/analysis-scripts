#!/usr/bin/python
'''USAGE: codonUsage.py fasta usage.txt
Counts codon usage in a nucleotide gene fasta
'''
import sys


# Counts codon usage in a single gene string
def countCodons(gene, codonDict, codons):

	gene = gene.upper()
	gene = [gene[i:i+3] for i in range(0, len(gene), 3)]

	for codon in gene:
		if len(codon) < 3:
			continue

		if not codon in codons:
			codonDict[codon] = 1
			codons.add(codon)
		else:
			codonDict[codon] += 1

	return(codonDict, codons)


# Read through and format nucleotide fasta, counting codons along the way
with open(sys.argv[1], 'r') as inFasta:

	seq = ''
	condons = {}
	codonSet = set()

	for line in inFasta:

		if line[0] == '>':
			condons, codonSet = countCodons(seq, condons, codonSet)
			seq = ''
			continue
		else:
			seq += line.strip()

condons, codonSet = countCodons(seq, condons, codonSet)


# Write codon counts to a 2 column file
with open(sys.argv[2], 'w') as outFile:
	for index in condons.keys():
		entry = index + '\t' + str(condons[index]) + '\n'
		outFile.write(entry)


