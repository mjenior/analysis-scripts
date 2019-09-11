
import sys

tax_counts = {}
with open(sys.argv[1], 'r') as fasta:

	for line in fasta:
		tax_id = line.split('|')[0]

		if ':' not in tax_id:
			continue
		else:
			tax_id = tax_id.split(':')[0].replace('>','')

			try:
				tax_counts[tax_id] += 1
			except KeyError:
				tax_counts[tax_id] = 1


ranked = sorted(tax_counts, key=tax_counts.get, reverse=True)[1:5]
for tax in ranked:
	print(tax + '\t' + str(tax_counts[tax]))
