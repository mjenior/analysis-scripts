#!/usr/bin/python
'''USAGE: revComp.py Nucleotide_sequence
This script returns the reverse complement .
'''
import sys

compDict = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
seq = list(str(sys.argv[1]).upper())
rev = []

for nuc in seq:
	rev.append(compDict[nuc])

rev = ''.join(list(reversed(rev)))
print(rev)
