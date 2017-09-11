#!/usr/bin/python2.7
'''USAGE: fasta_stats.py seqFile
This script calculates various statistics about the provided fasta or fastq file.
'''
import sys
import os

# This function reads in fasta file, appends the length of each sequence to a list, and counts all Gs & Cs.
        # It returns a sorted list of sequence lengths with the G+C % as the last element.
def read_lengths(fasta):

        len_list = []
        gc_count = 0
        for line in fasta:
                if line == '\n':
                        continue
                elif line[0] == '>':
                        continue
                else:
                        len_list.append(len(line.strip()))
                        gc_count += line.upper().count('G') + line.upper().count('C')
        
        gc_percent = round(((gc_count / sum(len_list)) * 100), 2)

        return(len_list, gc_percent)

# This function calculates and returns all the printed statistics.
def calc_stats(lengths):

        lengths.sort()
        shortest = lengths[0]
        longest = lengths[-1]
        total_contigs = len(lengths) # Total number of sequences
        len_sum = sum(lengths) # Total number of residues
        total_Mb = len_sum/1000000.00 # Total number of residues expressed in Megabases
        if len_sum == 0: len_sum = 1

        # interquartile range
        if total_contigs >= 4:
                median_len = lengths[int(round(total_contigs/2))] # Median sequence length
                q1_range = lengths[0:(int(total_contigs/2)-1)]
                if len(q1_range) == 0:
                        q1 = lengths[0]
                else:
                        q1 = q1_range[int(len(q1_range)/2)]
                q3_range = lengths[(int(total_contigs/2)+1):-1]
                if len(q3_range) == 0:
                        q3 = lengths[-1]
                else:
                        q3 = q3_range[int(len(q3_range)/2)]
                iqr = int(q3 - q1)
        else:
                iqr = 'Too few sequences to calculate'
                median_len = 'Too few sequences to calculate'

        #n50 calculation loop
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

        if total_contigs < 4:
                n50 = 'Too few sequences to calculate'
                n90 = 'Too few sequences to calculate'
                l50 = 'Too few sequences to calculate'
        else:
                l50 = lengths.count(n50)

        return(total_contigs, total_Mb, n50, l50, n90, median_len, iqr, seqs_1000, seqs_5000, shortest, longest)

#----------------------------------------------------------------------------------------#

if os.stat(str(sys.argv[1])).st_size == 0:
        print('ERROR: Empty input file.')
        sys.exit()

with open(sys.argv[1], 'r') as contigs:
        contig_lengths = read_lengths(open(sys.argv[1], 'r'))

stat_list = calc_stats(contig_lengths[0])

output_string = """# Input file name: {filename}
# Total contigs: {total_contigs}
# Total bases: {total_mb} Mb
# Sequence N50: {n50}
# Sequence L50: {l50}
# Sequence N90: {n90}
# Median sequence length: {median_len}
# Interquartile range: {iqr}
# Shortest sequence length: {short}
# Longest sequence length: {long}
# Sequences > 1 kb: {seqs_1k}
# Sequences > 5 kb: {seqs_5k}
# GC content: {gc}%
""".format(filename = str(sys.argv[1]).split('/')[-1],  
        total_contigs = stat_list[0], 
        total_mb = "%.2f" % stat_list[1], 
        n50 = stat_list[2],
        l50 = stat_list[3],
        n90 = stat_list[4],
        median_len = stat_list[5], 
        iqr = stat_list[6], 
        short = stat_list[9], 
        long = stat_list[10],  
        seqs_1k = stat_list[7], 
        seqs_5k = stat_list[8],
        gc = contig_lengths[1])

print output_string

