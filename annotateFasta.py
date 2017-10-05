#!/usr/bin/python
'''USAGE: annotateFasta.py BLASToutput Fasta
This script annotates a fasta file with sequence names determined from a BLAST of that file.
'''
import sys

# Write dictionary from BLAST output
with open(sys.argv[1],'r') as blast_output:
        blast_dictionary = {}
        gene_count = 0
        for line in blast_output:
                gene_count += 1
                line = line.split()
                entry = line[1] + '|Evalue:' + str(line[10]) + '|gene:' + str(gene_count).zfill(9)
                blast_dictionary[line[0]] = entry


# Parse the fasta file and print translated names and unchanged sequence data
with open(sys.argv[2],'r') as input_fasta:
        outfile_name = str(sys.argv[2]).rstrip('fastn') + 'annotated.fasta'
        output_fasta = open(outfile_name, 'w')

        key_errors = 0
        for line in input_fasta:

                if str(line)[0] == '>':
                        entry = str(line).strip('>').strip()

                        try:
                                blast_hit = blast_dictionary[entry]
                        except KeyError:
                                key_errors += 1
                                blast_hit = entry + '|unknown:' + str(key_errors).zfill(9)

                        final_entry = '>' + blast_hit + '\n'
                        output_fasta.write(final_entry)
                        continue

                else:
                        output_fasta.write(line)

output_fasta.close()

