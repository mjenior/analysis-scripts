#!/usr/bin/env python
# USAGE: makeFiles.py file_name

import sys
import glob

with open(sys.argv[1], 'w') as outFile:
        fastqR1 = glob.glob('*_R1_*.fastq')
        for R1 in fastqR1:
                entry = str(R1).split('_')[0] + '\t' + R1 + '\t' + R1.replace('_R1_','_R2_') + '\n'
                outFile.write(entry)

