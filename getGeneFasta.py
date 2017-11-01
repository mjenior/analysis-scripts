#!/usr/bin/python
'''USAGE: getGeneFasta.py annotation genome
This script creates a nucleotide fasta of gene sequences based on annotation and complete genome
'''
import sys


def revComp(sequence):

	# Pyrimidines
	sequence.replace('A', 'X')
	sequence.replace('T', 'A')
	sequence.replace('X', 'T')
	#Purines
	sequence.replace('C', 'X')
	sequence.replace('G', 'C')
	sequence.replace('X', 'G')

	return(sequence)


def readAnnotation(annotation):




