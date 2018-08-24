#!/usr/bin/python
'''USAGE: sepReports.py pooled_reports output.tsv
This script separates pooled assembly quality statistics into distinct tables
'''
import sys

with open(sys.argv[1], 'r') as report:

	assembly = ['Assembly']
	contigs = ['Contigs']
	bases = ['Bases(Mb)']
	ns = ['Ns']
	gc = ['G+C(%)']
	n50 = ['N50']
	l50 = ['L50']
	n90 = ['N90']
	medians = ['Median']
	q1 = ['Q1']
	q3 = ['Q3']
	iqr = ['IQR']
	means = ['Mean']
	std = ['Std']
	skew = ['Skewness']
	shortest = ['Shortest']
	longest = ['Longest']
	small = ['Contigs<1kb']
	kb1 = ['Contigs>1kb']
	kb5 = ['Contigs>5kb']
	kb10 = ['Contigs>10kb']

	for line in report:

		if line == '\n':
			continue

		line = line.split()
		if line[0] == 'Assembly:':
			assembly.append(str(line[1]))
			continue
		elif line[0] == 'Contigs:':
			contigs.append(str(line[1]))
			continue
		elif line[0] == 'Bases(Mb):':
			bases.append(str(line[1]))
			continue
		elif line[0] == 'Ns:':
			ns.append(str(line[1]))
			continue
		elif line[0] == 'G+C(%):':
			gc.append(str(line[1]))
			continue
		elif line[0] == 'N50:':
			n50.append(str(line[1]))
			continue
		elif line[0] == 'L50:':
			l50.append(str(line[1]))
			continue
		elif line[0] == 'N90:':
			n90.append(str(line[1]))
			continue
		elif line[0] == 'Median:':
			medians.append(str(line[1]))
			continue
		elif line[0] == 'Q1:':
			q1.append(str(line[1]))
			continue
		elif line[0] == 'Q3:':
			q3.append(str(line[1]))
			continue
		elif line[0] == 'IQR:':
			iqr.append(str(line[1]))
			continue
		elif line[0] == 'Mean:':
			means.append(str(line[1]))
			continue
		elif line[0] == 'Std:':
			std.append(str(line[1]))
			continue
		elif line[0] == 'Skewness:':
			skew.append(str(line[1]))
			continue
		elif line[0] == 'Shortest:':
			shortest.append(str(line[1]))
			continue
		elif line[0] == 'Longest:':
			longest.append(str(line[1]))
			continue
		elif line[0] == 'Contigs<1kb:':
			small.append(str(line[1]))
			continue
		elif line[0] == 'Contigs>1kb:':
			kb1.append(str(line[1]))
			continue
		elif line[0] == 'Contigs>5kb:':
			kb5.append(str(line[1]))
			continue
		elif line[0] == 'Contigs>10kb:':
			kb10.append(str(line[1]))
			continue
		else:
			continue

with open(sys.argv[2], 'w') as stats:

	assembly = '\t'.join(assembly) + '\n'
	stats.write(assembly)
	contigs = '\t'.join(contigs) + '\n'
	stats.write(contigs)
	bases = '\t'.join(bases) + '\n'
	stats.write(bases)
	ns = '\t'.join(ns) + '\n'
	stats.write(ns)
	gc = '\t'.join(gc) + '\n'
	stats.write(gc)
	n50 = '\t'.join(n50) + '\n'
	stats.write(n50)
	l50 = '\t'.join(l50) + '\n'
	stats.write(l50)
	n90 = '\t'.join(n90) + '\n'
	stats.write(n90)
	medians = '\t'.join(medians) + '\n'
	stats.write(medians)
	q1 = '\t'.join(q1) + '\n'
	stats.write(q1)
	q3 = '\t'.join(q3) + '\n'
	stats.write(q3)
	iqr = '\t'.join(iqr) + '\n'
	stats.write(iqr)
	means = '\t'.join(means) + '\n'
	stats.write(means)
	std = '\t'.join(std) + '\n'
	stats.write(std)
	skew = '\t'.join(skew) + '\n'
	stats.write(skew)
	shortest = '\t'.join(shortest) + '\n'
	stats.write(shortest)
	longest = '\t'.join(longest) + '\n'
	stats.write(longest)
	small = '\t'.join(small) + '\n'
	stats.write(small)
	kb1 = '\t'.join(kb1) + '\n'
	stats.write(kb1)
	kb5 = '\t'.join(kb5) + '\n'
	stats.write(kb5)
	kb10 = '\t'.join(kb10) + '\n'
	stats.write(kb10)
