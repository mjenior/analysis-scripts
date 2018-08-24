#!/usr/bin/python
# -*- coding: utf-8 -*-
'''USAGE: formatContigs.py fasta
Reformats fasta files for downstream use
'''
import sys
import math
import argparse

# This function reads in fasta file, appends the length of each sequence to a list, and counts all Gs & Cs.
	# It returns a sorted list of sequence lengths with the G+C % as the last element.
def readFasta(fastaFile, outFile, minLen, maxLen):

	lenLst = []
	GC = 0
	N = 0
	allNuc = 0
	skip = 0
	seq = ''

	name = 'foo'
	while name[0] != '>':
		name = fastaFile.readline()
	name = name.replace(' ', '_').replace('|', '__').replace(',', '_')

	for line in fastaFile:
		if line[0] == '>': 
			if len(seq) >= minLen and len(seq) <= maxLen:
				GC += (seq.count('G') + seq.count('C'))
				N += seq.count('N')
				allNuc += len(seq)
				lenLst.append(len(seq))
				outFile.write(name)
				name = line.replace(' ', '_').replace('|', '__').replace(',', '_')
				seq += '\n\n'
				outFile.write(seq)
				continue
			else:
				skip += 1
			seq = ''
			continue
		else:
			seq += line.strip().upper()

	lenLst.sort()

	return(lenLst, GC, N, skip)


# Function t0 calculate standard deviation for a list of numbers
def standDev(values):
	x_mean = sum(values) / len(values)
	sd_list = []
	for x in values:
		y = (x - x_mean) ** 2
		sd_list.append(y)
	y_mean = sum(sd_list) / len(sd_list)   
	sd = math.sqrt(y_mean)
	return(sd)


# This function calculates and returns all the printed statistics.
def calc_stats(lengths, ns, gc):

	shortest = lengths[0]
	longest = lengths[-1]
	total_contigs = len(lengths) # Total number of sequences
	len_sum = sum(lengths) # Total number of residues
	total_Mb = len_sum/1000000.00 # Total number of residues expressed in Megabases
	mid_pos = int(round(total_contigs/2))

	median_len = lengths[mid_pos] # Median sequence length
	q1 = lengths[0:mid_pos][int(len(lengths[0:mid_pos])/2)]
	q3 = lengths[mid_pos:-1][int(len(lengths[mid_pos:-1])/2)]
	iqr = q3 - q1

	mean_len = sum(lengths) / len(lengths)
	sd = standDev(lengths)

	# Pearson’s Coefficient of Skewness
	skew = ((mean_len - median_len) * 3) / sd
	mean_len = round(mean_len, 2)
	sd = round(sd, 2)
	skew = round(skew, 3)
 
	current_bases = 0
	n50 = 0
	n90 = 0
	seqs_1000 = 0
	seqs_5000 = 0
	seqs_10000 = 0
	percent50_bases = int(round(len_sum*0.5))
	percent90_bases = int(round(len_sum*0.1))

	for x in lengths:

		current_bases += x

		if x > 1000:
			seqs_1000 += 1
		if x > 5000:
			seqs_5000 += 1
		if x > 10000:
			seqs_10000 += 1

		if current_bases >= percent50_bases and n50 == 0:
			n50 = x
		if current_bases >= percent90_bases and n90 == 0:
			n90 = x

	l50 = lengths.count(n50)
	short_contigs = total_contigs - seqs_1000

	outputStr = """
# Assembly name:	{filename}
# Total contigs:	{total_contigs}
# Total bases (Mb):	{total_mb}
# Ns:	{ns}
# G+C content (%):	{gc}
--------------------------------
# N50:	{n50}
# L50:	{l50}
# N90:	{n90}
--------------------------------
# Median length:	{median_len}
# Q1:	{q1}
# Q3:	{q3}
# IQR:	{iqr}
# Mean length:	{mean}
# Standard deviation:	{sd}
# Skewness:	{skewness}
--------------------------------
# Shortest length:	{short}
# Longest length:	{long}
# Contigs < 1 kb:	{short_contigs}
# Contigs > 1 kb:	{seqs_1k}
# Contigs > 5 kb:	{seqs_5k}
# Contigs > 10 kb:	{seqs_10k}

""".format(filename = str(sys.argv[1]).split('/')[-1],  
	total_contigs = total_contigs, 
	total_mb = "%.2f" % total_Mb, 
	n50 = n50,
	l50 = l50,
	n90 = n90,
	median_len = median_len, 
	q1 = q1, 
	q3 = q3,
	iqr = iqr,
	mean = mean_len,
	sd = sd,
	skewness = skew,
	short = shortest, 
	long = longest,
	short_contigs = short_contigs, 
	seqs_1k = seqs_1000, 
	seqs_5k = seqs_5000,
	seqs_10k = seqs_10000,
	gc = gc,
	ns = ns)

	with open('summary.txt', 'w') as statsReport:
		statsReport.write(outputStr)


#------------------------------------------------------------------------------------------------------------------------------------#

# User defined arguments
parser = argparse.ArgumentParser(description='Reformats a fasta file for easier downstream use in other bioinformatic platforms.')
parser.add_argument('inputFile')
parser.add_argument('--out', default='formatted.fasta', help='Name of output file')
parser.add_argument('--min', default=0, help='Minimum length of sequences to be included')
parser.add_argument('--max', default=999999999, help='Maximum length of sequences to be included')
parser.add_argument('--stats', default='n', help='Calculate summary statistics for input fasta')
args = parser.parse_args()

# Assign variables
inputFasta = str(args.inputFile)
outputFasta = str(args.out)
minLen = int(args.min)
maxLen = int(args.max)
calcStats = str(args.stats)

#------------------------------------------------------------------------------------------------------------------------------------#


with open(inputFasta, 'r') as inputFile:
	with open(outputFasta, 'w') as outputFile:
		lenLst, GCs, Ns, skip = readFasta(inputFile, outputFile, minLen, maxLen)
	if calcStats == 'y':
		calc_stats(lenLst, Ns, GCs)


if minLen != 0 or maxLen != 999999999:
	print('Included sequences: ' + str(len(lenLst)))
	print('Omitted sequences: ' + str(skip))



