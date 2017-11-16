#!/usr/bin/env python
# USAGE: makeFiles.py file_name

import sys
import glob

fastqR1 = glob.glob('*R1*')

with open(sys.argv[1], 'w') as outFiles:

	for R1 in fastqR1:
		name = str(R1).split('_')[0]
		R2 = R1.replace('R1','R2')
		entry = name + '\t' + R1 + '\t' + R2 + '\n'
		outFiles.write(entry)

