#!/usr/bin/env python
# USAGE: normIDX.py input_file 250 y
# Normalizes read abundances and removes targets with no mappings (optional)

import sys

with open(sys.argv[1], 'r') as idxstats:

        outfile = str(sys.argv[1]).rstrip('tcsvx') + 'norm_idx.tsv'
        outfile = open(out_str, 'w')
        outfile.write('gene_target\tnormalized_read_abundances\n')

        read_len = int(sys.argv[2])
        include = str(sys.argv[3])
        mapped = 0

        for line in idxstats:

                if line[0] == '*':
                        unmapped = int(line.split()[3])
                        continue

                elif int(line.split()[2]) != 0 or include == 'y':
                        target = str(line.split()[0])
                        mapped += int(line.split()[2])
                        normalized = str((int(line.split()[2]) * read_len) / int(line.split()[1]))
                        entry = target + '\t' + normalized + '\n'
                        outfile.write(entry)

print(str((mapped/(mapped+unmapped))*100) + '% mapped')
outfile.close()
