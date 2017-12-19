#!/usr/bin/env python
# USAGE: makeFiles.py file_name

import sys
import glob

with open(sys.argv[1], 'w') as outFiles:
	fastqR1 = glob.glob('*R1*.fastq')
	for R1 in fastqR1:
		entry = str(R1).split('_')[0] + '\t' + R1 + '\t' + R1.replace('R1','R2') + '\n'
		outFiles.write(entry)

