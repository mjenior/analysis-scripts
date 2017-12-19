#!/usr/bin/python2.7
'''USAGE: fasta_stats.py seqFile
This script calculates various statistics about the provided fasta or fastq file.
'''
import sys

# This function reads in fasta file, appends the length of each sequence to a list, and counts all Gs & Cs.
        # It returns a sorted list of sequence lengths with the G+C % as the last element.
def read_lengths(fasta):

        len_lst = []
        gc_cnt = 0
        all_cnt = 0
        for line in fasta:
                if line == '\n' or line[0] == '>': continue
                line = line.strip().upper()
                gc_cnt += line.count('G')
                gc_cnt += line.count('C')
                all_cnt += len(line)
                len_lst.append(len(line))

        gc_prcnt = str(round((float(gc_cnt) / float(all_cnt)) * 100.0, 2))
        len_lst.sort()

        return(len_lst, gc_prcnt)

# This function calculates and returns all the printed statistics.
def calc_stats(lengths):

        shortest = lengths[0]
        longest = lengths[-1]
        total_contigs = len(lengths) # Total number of sequences
        len_sum = sum(lengths) # Total number of residues
        total_Mb = len_sum/1000000.00 # Total number of residues expressed in Megabases
        mid_pos = int(round(total_contigs/2))

        median_len = lengths[mid_pos] # Median sequence length
        q1 = lengths[0:mid_pos][int(len(lengths[0:mid_pos])/2)]
        q3 = lengths[mid_pos:-1][int(len(lengths[mid_pos:-1])/2)]
 
        current_bases = 0
        n50 = 0
        n90 = 0
        seqs_1000 = 0
        seqs_5000 = 0
        percent50_bases = int(round(len_sum*0.5))
        percent90_bases = int(round(len_sum*0.1))

        for x in lengths:

                current_bases += x

                if x > 1000:
                        seqs_1000 += 1
                if x > 5000:
                        seqs_5000 += 1

                if current_bases >= percent50_bases and n50 == 0:
                        n50 = x
                if current_bases >= percent90_bases and n90 == 0:
                        n90 = x

        l50 = lengths.count(n50)

        return(total_contigs, total_Mb, n50, l50, n90, median_len, q1, q3, seqs_1000, seqs_5000, shortest, longest)

#----------------------------------------------------------------------------------------#

with open(sys.argv[1], 'r') as contigs:
        contig_lengths, gc_content = read_lengths(open(sys.argv[1], 'r'))

stat_list = calc_stats(contig_lengths)

output_string = """
# Assembly name: {filename}
# Total contigs: {total_contigs}
# Total bases: {total_mb} Mb
# G+C content: {gc}%
# N50: {n50}
# L50: {l50}
# N90: {n90}
# Median length: {median_len}
# Q1: {q1}
# Q3: {q3}
# Shortest length: {short}
# Longest length: {long}
# Contigs > 1 kb: {seqs_1k}
# Contigs > 5 kb: {seqs_5k}
""".format(filename = str(sys.argv[1]).split('/')[-1],  
        total_contigs = stat_list[0], 
        total_mb = "%.2f" % stat_list[1], 
        n50 = stat_list[2],
        l50 = stat_list[3],
        n90 = stat_list[4],
        median_len = stat_list[5], 
        q1 = stat_list[6], 
        q3 = stat_list[7],
        short = stat_list[10], 
        long = stat_list[11],  
        seqs_1k = stat_list[8], 
        seqs_5k = stat_list[9],
        gc = gc_content)

print(output_string)
