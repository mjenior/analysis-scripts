#!/usr/bin/env python
# USAGE: python checkBins.py binned_fasta
# Checks binned contig files for purity

import sys

def calcStats(lengths):

        total_seq = len(lengths)
        total_Mb = sum(lengths)/1000000.00
        total_Mb = "%.2f" % total_Mb

        lengths.sort()
        shortest = lengths[0]
        longest = lengths[-1]
        median_len = lengths[int(round(total_seq/2))] 
        q1 = lengths[int(round(len(lengths) * 0.25))]
        q3 = lengths[int(round(len(lengths) * 0.75))]

        current_bases = 0
        n50 = 0
        n90 = 0
        seqs_1k = 0
        seqs_5k = 0
        seqs_10k = 0
        percent50_bases = int(round(sum(lengths)*0.5))
        percent90_bases = int(round(sum(lengths)*0.1))

        for index in lengths:
        	current_bases += index
        	if index > 1000:
        		seqs_1k += 1
        		if index > 5000:
        			seqs_5k += 1
        			if index > 10000:
        				seqs_10k += 1

        	if current_bases >= percent50_bases and n50 == 0:
        		n50 = index
        		l50 = lengths.count(index)
        	if current_bases >= percent90_bases and n90 == 0:
        		n90 = index

        return(total_seq, total_Mb, n50, n90, median_len, q1, q3, seqs_1k, seqs_5k, seqs_10k, shortest, longest)


with open(sys.argv[1], 'r') as binned_contigs:

	entry_lst = []
	len_lst = []

	for line in binned_contigs:

		if line == '\n':
			continue

		elif line[0] == '>':
			entry = line.split('_')[0]
			entry = entry.lstrip('>')
			entry_lst.append(entry)
			continue

		else:
			len_lst.append(len(line.strip()))


unique_entries = len(list(set(entry_lst)))
most_frequent = max(set(entry_lst), key=entry_lst.count)
count_frequent = entry_lst.count(most_frequent)
contamination = (float((len(entry_lst) - count_frequent)) / float(len(entry_lst))) * 100.0
contamination = "%.3f" % contamination

stat_list = calcStats(len_lst)

output_string = """# Binned contig file: {fasta}
# Unique sources: {uniques}
# Most frequent source: {frequent}
# Total from most frequent: {top_freq}
# Contaminants: {contam} %

# Total contigs: {total_seq}
# Total bases: {total_mb} Mb
# N50: {n50}
# N90: {n90}
# Median length: {med_len}
# Q1: {q1}
# Q3: {q3}
# Contigs > 1 kb: {seqs_1k}
# Contigs > 5 kb: {seqs_5k}
# Contigs > 10 kb: {seqs_10k}
# Shorest contig: {shortest}
# Longest contig: {longest}

#-----------------------------------------#
""".format(fasta = str(sys.argv[1]),
	uniques = str(unique_entries),
	frequent = str(most_frequent),
	top_freq = str(count_frequent),
	contam = str(contamination),
	total_seq = str(stat_list[0]), 
	total_mb = str(stat_list[1]),
	n50 = str(stat_list[2]),
	n90 = str(stat_list[3]),
	med_len = str(stat_list[4]),
	q1 = str(stat_list[5]),
	q3 = str(stat_list[6]),
	seqs_1k = str(stat_list[7]),
	seqs_5k = str(stat_list[8]),
	seqs_10k = str(stat_list[9]),
	shortest = str(stat_list[10]),
	longest = str(stat_list[11]))

print output_string
