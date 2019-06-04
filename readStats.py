#!/usr/bin/python
'''USAGE: readStats.py fastq
Reports stats for fastq files
'''
import sys

def read_lengths(fastq):

        line_count = 3
        len_list = []

        for line in fastq:

                line_count += 1
                if line_count == 5:
                        len_list.append(len(line.strip()))
                        line_count = 1

        return(len_list)


def calc_stats(lengths):

        lengths.sort()

        total_reads = len(lengths) # Total number of sequences
        total_Mb = sum(lengths)/1000000.00 # Total number of residues (Mb)
        shortest_read = lengths[0]
        longest_read = lengths[-1]

        # interquartile range
        if total_reads >= 4:

                median_len = lengths[int(round(total_reads/2))]
                mode_len = max(set(lengths), key=lengths.count)
                mode_count = lengths.count(mode_len)
                
        else:
                mode_len = 'Too few sequences to calculate'
                mode_count = 'Too few sequences to calculate'
                median_len = 'Too few sequences to calculate'

        return([total_reads, total_Mb, shortest_read, longest_read, median_len, mode_len, mode_count])


read_lens = read_lengths(open(sys.argv[1], 'r'))

stat_lst = calc_stats(read_lens)

output_str = """
# Input file name:\t{filename}
# Total reads:\t{reads}
# Total bases (Mb):\t{mb} 
# Shortest read length:\t{short}
# Longest read length:\t{long}
# Median read length:\t{med}
# Mode read length:\t{mode}
# Mode frequency:\t{mode_freq}
""".format(filename = str(sys.argv[1]).split('/')[-1],
        reads = stat_lst[0],
        mb = "%.2f" % stat_lst[1],
        short = stat_lst[2],
        long = stat_lst[3],
        med = stat_lst[4],
        mode = stat_lst[5],
        mode_freq = stat_lst[6])

print output_str

