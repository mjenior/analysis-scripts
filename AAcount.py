
import sys

translationDict = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}

abbreviationDict = {'A':'Alanine','R':'Arginine','N':'Asparagine','D':'Aspartic acid','C':'Cysteine',
'E':'Glutamic acid','Q':'Glutamine','G':'Glycine','H':'Histidine','I':'Isoleucine','L':'Leucine',
'K':'Lysine','M':'Methionine','F':'Phenylalanine','P':'Proline','S':'Serine','T':'Threonine',
'W':'Tryptophan','Y':'Tyrosine','V':'Valine'}

def translateDNA(sequence):
	codons = [sequence[x:x+3] for x in range(0, len(sequence), 3)]
	peptide = [translationDict[y] for y in codons]
	return peptide


AAcounts = {}
total_AA = 0
with open(sys.argv[1], 'r') as fasta:
	
	seq = ''
	firstLine = 'placeholder'
	while firstLine[0] != '>' or firstLine == '\n': firstLine = fasta.readline()

	for line in fasta:
		if line[0] == '>':
			pep = translateDNA(seq)
			for aa in pep:
				if aa == '_':
					continue
				else:
					total_AA += 1
                	try:
                    	AAcounts[aa] += 1
                	except KeyError:
                    	AAcounts[aa] = 1
			seq = ''
		else:
			seq += line.strip().upper()


for aa in AAcounts.keys(): 
	norm_count = float(AAcounts[aa]) / float(total_AA)
	norm_count = round(norm_count, 3)
	print(abbreviationDict[aa] + '\t' + str(norm_count))