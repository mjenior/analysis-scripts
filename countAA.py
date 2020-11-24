
import sys

abbreviationDict = {'A':'Alanine','R':'Arginine','N':'Asparagine','D':'Aspartic acid','C':'Cysteine','E':'Glutamic acid',
'Q':'Glutamine','G':'Glycine','H':'Histidine','I':'Isoleucine','L':'Leucine','K':'Lysine','M':'Methionine','F':'Phenylalanine',
'P':'Proline','S':'Serine','T':'Threonine','W':'Tryptophan','Y':'Tyrosine','V':'Valine','U':'Selenocysteine','O':'Pyrrolysine'}
AAcounts = {'A':0,'R':0,'N':0,'D':0,'C':0,'Q':0,'E':0,'G':0,'H':0,'I':0,'L':0,'K':0,'M':0,'F':0,'P':0,'O':0,'S':0,'U':0,'T':0,'W':0,'Y':0,'V':0}

total_AA = 0
with open(sys.argv[1], 'r') as fasta:
	
	seq = ''
	firstLine = 'placeholder'
	while firstLine[0] != '>' or firstLine == '\n': firstLine = fasta.readline()

	for line in fasta:
		if line[0] == '>':
			seq = list(seq)
			for aa in seq:
				total_AA += 1
				if aa == 'J':
					AAcounts['I'] += 1
					AAcounts['L'] += 1
				elif aa == 'B':
					AAcounts['D'] += 1
					AAcounts['E'] += 1
				elif aa == 'Z':
					AAcounts['E'] += 1
					AAcounts['Q'] += 1
				elif aa == 'X':
					for x in AAcounts.keys():
						AAcounts[x] += 1
				else:
					AAcounts[aa] += 1
			seq = ''
		else:
			seq += line.strip().upper()

for aa in AAcounts.keys(): 
	norm_count = float(AAcounts[aa]) / float(total_AA)
	norm_count = norm_count * 5.
	norm_count = round(norm_count, 3)
	if norm_count == 0.0: continue
	print(abbreviationDict[aa] + '\t' + str(norm_count))

