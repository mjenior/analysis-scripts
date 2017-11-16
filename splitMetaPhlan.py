#!/usr/bin/python
'''USAGE: splitMetaPhlan.py MetaPhlanOutput
Reformats MetaPhlan output to focus on Bacteria at each taxonomic level
'''
import sys


# Read MetaPhlan results and create a dictionary at the correct taxonomic level
with open(sys.argv[1],'r') as metaphlan:

        phylum_dict = {}
        class_dict = {}
        order_dict = {}
        family_dict = {}
        genus_dict = {}
        species_dict = {}

        for line in metaphlan:
                if line[0] == '#': continue
                
                line = line.split()
                tax = line[0].split('|')
                relabund = float(line[1])
                if tax[0] != 'k__Bacteria': continue
                
                if len(tax) == 2:
                        taxon = tax[1].split('__')[1]                
                        try:
                                phylum_dict[taxon] = phylum_dict[taxon] + relabund
                        except KeyError:
                                phylum_dict[taxon] = relabund

                elif len(tax) == 3:
                        taxon = tax[2].split('__')[1]                
                        try:
                                class_dict[taxon] = class_dict[taxon] + relabund
                        except KeyError:
                                class_dict[taxon] = relabund

                elif len(tax) == 4:
                        taxon = tax[3].split('__')[1]                
                        try:
                                order_dict[taxon] = order_dict[taxon] + relabund
                        except KeyError:
                                order_dict[taxon] = relabund

                elif len(tax) == 5:
                        taxon = tax[4].split('__')[1]                
                        try:
                                family_dict[taxon] = family_dict[taxon] + relabund
                        except KeyError:
                                family_dict[taxon] = relabund

                elif len(tax) == 6:
                        taxon = tax[5].split('__')[1]                
                        try:
                                genus_dict[taxon] = genus_dict[taxon] + relabund
                        except KeyError:
                                genus_dict[taxon] = relabund

                elif len(tax) == 7:
                        taxon = tax[6].split('__')[1]                
                        try:
                                species_dict[taxon] = species_dict[taxon] + relabund
                        except KeyError:
                                species_dict[taxon] = relabund



# NEED TO WRITE TAXONMOY FILE!!!!!!



# Recalculate new relative abundances and write to a file
all_tax = ['phylum', 'class', 'order', 'family', 'genus', 'species']
dict_lst = [phylum_dict, class_dict, order_dict, family_dict, genus_dict, species_dict]
for tax_lvl in range(0, 6):
        outname = str(sys.argv[1]).rstrip('txsv') + 'bact.' + all_tax[tax_lvl] + '.tsv'
        with open(outname, 'w') as outfile:
                entry = all_tax[tax_lvl].title() + '\tRel_Abund\n'
                outfile.write(entry)
                total_bact = sum(dict_lst[tax_lvl].values())

                for index in dict_lst[tax_lvl].keys():
                        new_relabund = (dict_lst[tax_lvl][index] / total_bact) * 100
                        entry = index + '\t' + str(new_relabund) + '\n'
                        outfile.write(entry)

