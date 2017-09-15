#!/usr/bin/env python
# USAGE: makeFiles.py file_name

import sys
from os
from os.path import isfile, join

fastqs = [x for x in os.listdir(str(os.getcwd())) if isfile(join(str(os.getcwd()), x))]
fastqs = list(set(fastqs))

with open(sys.argv[1], 'w') as out_files:

	for index in fastqs:
		entry = str(index).split('.')[0]
		entry = entry + '\t' + entry + '.R1.fastq\t' + entry + '.R2.fastq\n'
		out_files.write(entry)

