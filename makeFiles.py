#!/usr/bin/env python
# USAGE: makeFiles.py file_name

import sys
import glob

with open(sys.argv[1], 'w') as outFiles:
	fastqR1 = glob.glob('*.1.fq')
	for R1 in fastqR1:
		entry = str(R1).split('.')[2] + '\t' + R1 + '\t' + R1.replace('.1.','.2.') + '\n'
		outFiles.write(entry)

