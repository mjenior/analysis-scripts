#!/usr/bin/python
'''USAGE: 


'''
import sys
import numpy
import copy
from scipy.stats import wilcoxon

import cobra
import cobra.test
import cobra.util.solver
from cobra.manipulation.delete import *


def read_transcription(filename, sep='\t'):

	abund_dict = {}
	with open(filename, 'r') as transcription:

		for line in transcription:
			line = line.split(sep)

			gene = str(line[0])
			abundances = [float(x) for x in line[1:]]
			abund_dict[gene] = abundances

	return abund_dict


def test_differences(condition1, condition2):

	change_dict = {}
	genes = set(list(condition1.keys()) + list(condition2.keys()))
	for gene in genes:
		try:
			curr_cond1 = condition1[gene]
		except KeyError:
			continue
		try:
			curr_cond2 = condition2[gene]
		except KeyError:
			continue

		pval = round(float(wilcoxon(curr_cond1, curr_cond2).pvalue), 3)

		if numpy.median(curr_cond1) - numpy.median(curr_cond2) < 0.0:
			diff = 1
		elif numpy.median(curr_cond1) - numpy.median(curr_cond2) > 0.0:
			diff = -1
		else:
			diff = 0

		change_dict[gene] = [diff, pval]

	return change_dict





def parse_gpr(str_expr):
    """parse gpr into AST

    Parameters
    ----------
    str_expr : string
        string with the gene reaction rule to parse

    Returns
    -------
    tuple
        elements ast_tree and gene_ids as a set
    """
    str_expr = str_expr.strip()
    if len(str_expr) == 0:
        return None, set()


    tree = ast_parse(escaped_str, "<string>", "eval")
    cleaner = GPRCleaner()
    cleaner.visit(tree)
    eval_gpr(tree, set())  # ensure the rule can be evaluated
    return tree, cleaner.gene_set







# 
def parse_gpr_for_deletion(model, gene):

	# Identify 
	final_rxns = []
	curr_rxns = list(model.genes.get_by_id(gene).reactions)
	for rxn in curr_rxns:
		curr_rule = str(rxn.gene_reaction_rule).split()



		
    	try:
        	curr_rule = curr_rule.remove('(')
        	curr_rule = curr_rule.remove(')')
    	except:
        	pass
    	if test == None:
        	continue
    	if len(test) > 1:
        	print test





        else:
        	final_rxns.append(rxn.id)

	return final_rxns # list of reaction IDs


# 
def generate_models(model, change_dict, pvalue=0.05):

	condition1 = copy.deepcopy(model)
	condition2 = copy.deepcopy(model)

	for gene in change_dict.keys():
		curr_diff = change_dict[gene]

		if curr_diff[0] == 1 and curr_diff[1] <= pvalue:
			remove_rxns = parse_gpr_for_deletion(condition2, gene)
			for rxn in remove_rxns:
				condition2.reactions.get_by_id(rxn).remove_from_model(remove_orphans=True)
			continue
		elif curr_diff[0] == -1 and curr_diff[1] <= pvalue:
			remove_rxns = parse_gpr_for_deletion(condition1, gene)
			for rxn in remove_rxns:
				condition1.reactions.get_by_id(rxn).remove_from_model(remove_orphans=True)
			continue
		else:
			continue

	return condition1, condition2


# 
def MADE(model, transcription1, transcription2, pvalue):

	transcript_dict1 = read_transcription(transcription1)
	transcript_dict2 = read_transcription(transcription2)
	difference_dict = test_differences(transcript_dict1, transcript_dict2)

	condition1_model, condition2_model = generate_models(model, difference_dict, pvalue)

	return condition1_model, condition2_model



