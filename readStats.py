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

                median_len = lengths[int(round(total_reads/2))] # Median sequence length

                q1 = lengths[0:(int(total_reads/2)-1)]
                if len(q1) == 0:
                        q1 = lengths[0]
                else:
                        q1 = q1[int(len(q1)/2)]

                q3 = lengths[(int(total_reads/2)+1):-1]
                if len(q3) == 0:
                        q3 = lengths[-1]
                else:
                        q3 = q3[int(len(q3)/2)]
                iqr = int(q3 - q1)

        else:
                iqr = 'Too few sequences to calculate'
                median_len = 'Too few sequences to calculate'

        return([total_reads, total_Mb, shortest_read, longest_read, median_len, iqr])


read_lens = read_lengths(open(sys.argv[1], 'r'))

stat_lst = calc_stats(read_lens)

output_str = """# Input file name: {filename}
# Total reads: {reads}
# Total bases: {mb} Mb
# Shortest read length: {short}
# Longest read length: {long}
# Median read length: {med}
# Interquartile range: {iqr}
""".format(filename = str(sys.argv[1]).split('/')[-1],
        reads = stat_lst[0],
        mb = "%.2f" % stat_lst[1],
        short = stat_lst[2],
        long = stat_lst[3],
        med = stat_lst[4],
        iqr = stat_lst[5])

print output_str

