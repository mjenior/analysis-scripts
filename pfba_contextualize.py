#!/usr/bin/python
'''
Dante
Transcriptomic Integration via Stepwise Flux Minimization Thresholding based on Abundance Distribution

Please cite when using:
Jenior ML and Papin JA. (2018) DANTE. BioRxiv. DOI

Example usage 1:
my_model = cobra.io.read_sbml_model('my_model.sbml')
gene_bins = read_transcription_file('reads_to_genes.tsv', replicates=True)
reaction_bins = create_reaction_partitions(my_model, gene_bins)
contextualized_model = contextualize(my_model, reaction_bins, new_model_name)

Example usage 2:
my_model = cobra.io.read_sbml_model('my_model.sbml')
gene_bins = read_binning_file('gene_bins.tsv')
reaction_bins = create_reaction_partitions(my_model, gene_bins)
contextualized_model = contextualize(my_model, reaction_bins, new_model_name)
'''

# Dependencies
import numpy
import copy
import cobra
from cobra.util import solver
from optlang.symbolics import Zero
from itertools import chain
from cobra.manipulation.delete import *

# Read in transcriptomic read abundances, default is tsv with no header 
def read_transcription_file(read_abundances_file, replicates=False, header=False, sep='\t'):
    
    abund_dict = {}
    with open(read_abundances_file, 'r') as transcription:
        
        if header == True:
            header_line = transcription.readline()

        for line in transcription:
            line = line.split(sep)

            gene = str(line[0])
            if replicates == True:
                abundance = float(numpy.median([float(x) for x in line[1:]]))
            else:
                abundance = float(line[1])

            abund_dict[gene] = abundance

    return abund_dict


# Converts a dictionary of transcript distribution percentiles (defaults: 90th, 75th, & 50th)
def create_reaction_partitions(model, transcription, save_bins_as=False, high_cutoff=90, mid_cutoff=75, low_cutoff=50):
    
    # Define transcript abundance cutoffs
    distribution = transcription.values()
    perc_hi = numpy.percentile(distribution, high_cutoff)
    perc_mid = numpy.percentile(distribution, mid_cutoff)
    perc_lo = numpy.percentile(distribution, low_cutoff)
    
    # Write to file if defined by user
    if save_bins_as != False:
        perc_file = open(save_bins_as, 'w')

    percentile_dict = {}
    for gene in model.genes:
        
        # If current gene not in transciptomic profile, default to inclusion
        failed = 0
        try:
            test = transcription[gene.id]
        except KeyError:
            curr_percentile = 1
            failed = 1
            pass

        # Assign percentile grouping scores
        if failed == 0:
            if transcription[gene.id] >= perc_hi:
                curr_percentile = 1
            elif transcription[gene.id] < perc_hi and transcription[gene.id] >= perc_mid:
                curr_percentile = 2
            elif transcription[gene.id] < perc_mid and transcription[gene.id] >= perc_lo:
                curr_percentile = 3
            elif transcription[gene.id] < perc_lo and transcription[gene.id] >= 0.0:
                curr_percentile = 4

        # Write the binning results to a file if requested by the user
        if save_bins_as != False:
            entry = str(gene.id) + '\t' + str(curr_percentile) + '\n'
            perc_file.write(entry)

        # Converts genes into corresponding reactions and adds them to a dictionary
        for rxn in list(gene.reactions): 
            percentile_dict[rxn.id] = curr_percentile

    if save_bins_as != False:
        perc_file.close()

    return percentile_dict


# Read in user-defined/editted gene priority binning file
def read_binning_file(partition_file):

    bin_dict = {}
    with open(partition_file, 'r') as percentiles:
        for line in percentiles:
            line = line.split()
            bin_dict[line[0]] = float(line[1])

    return bin_dict


# Bin reactions based on their percentile transcription
def parse_reaction_binning(model, percentiles):

    include = set()
    exclude = set()
    perc_top = set()
    perc_hi = set()
    perc_mid = set()
    perc_lo = set()
    
    # Assign bins associated with each percentile of the read abundance distribution
    for rxn in model.reactions:
        try:
            test = percentiles[rxn.id]
        except KeyError:
            continue

        # Define those reactions not considered in minimization steps
        if percentiles[rxn.id] == 0:
            include |= set([rxn.id])
        elif percentiles[rxn.id] == 5:
            exclude |= set([rxn.id])

        # Remainder of reactions
        elif percentiles[rxn.id] == 1:
            perc_top |= set([rxn.id])
        elif percentiles[rxn.id] == 2:
            perc_hi |= set([rxn.id])
        elif percentiles[rxn.id] == 3:
            perc_mid |= set([rxn.id])
        elif percentiles[rxn.id] == 4:
            perc_lo |= set([rxn.id])

        else:
            include |= set([rxn.id]) # If not found, automatically include in final model

    return include, exclude, perc_top, perc_hi, perc_mid, perc_lo


# Determine those reactions that carry flux 
def pFBA_by_percent_of_optimum(model, rxn_ids, optimum_fraction, exclude_from_min=True):
    
    # Minimize flux through all reactions such that the fraction of objective optimum is still achieved
    remove_ids = set()
    with model as m:
        
        # Fix previous objective as constraint with threshold of predefined fraction of uncontexualized flux
        solver.fix_objective_as_constraint(m, fraction=optimum_fraction)
        
        # Formulate pFBA objective
        if exclude_from_min == True:
            rxn_vars = ((rxn.forward_variable, rxn.reverse_variable) for rxn in m.reactions if rxn.id not in rxn_ids)
            excl_rxn_vars = ((rxn.forward_variable, rxn.reverse_variable) for rxn in m.reactions if rxn.id in rxn_ids)
            excl_rxn_vars = chain(*excl_rxn_vars)
        else:
            rxn_vars = ((rxn.forward_variable, rxn.reverse_variable) for rxn in m.reactions)
        rxn_vars = chain(*rxn_vars)
        pfba_obj = m.problem.Objective(Zero, direction='min', sloppy=True)
        m.objective = pfba_obj
        
        # Set linear coefficients based on if they are to be excluded from minimization
        m.objective.set_linear_coefficients({x: 1.0 for x in rxn_vars})
        if exclude_from_min == True:
            m.objective.set_linear_coefficients({y: 0.0 for y in excl_rxn_vars})
        
        # Identify those reactions of interest that carry flux in pFBA solution
        solution = m.optimize()
        fluxes = solution.fluxes
        for reaction, flux in fluxes.items():
            if reaction in rxn_ids and abs(flux) < 1e-6:
                remove_ids |= set([reaction])
    
    # Report percentage to be pruned in each step
    #print(str(round(((float(len(remove_ids)) / float(len(rxn_ids))) * 100.0), 2)) + '%')
    
    return remove_ids


# Prune model and text that contextualized model is still able to grow
def prune_and_test(model, remove_rxn_ids):

    # Prune highlighted reactions from model, removing newly orphaned genes and metabolites
    for rxn in remove_rxn_ids:
        try:
            model.reactions.get_by_id(rxn).remove_from_model(remove_orphans=True)
        except:
            pass
    
    # Remove residual orphaned reactions and metabolites (just in case)
    unused_current_cpd = 1
    unused_current_rxn = 1
    while unused_current_cpd != 0 or unused_current_rxn != 0:
        unused_cpd = prune_unused_metabolites(model)
        unused_rxn = prune_unused_reactions(model)        
        unused_current_cpd = len(unused_cpd)
        unused_current_rxn = len(unused_rxn)
    
    # Check that prune model can still achieve flux through the objective (just in case)
    if model.slim_optimize() < 1e-6: 
        print('WARNING: Pruned model objective can no longer carry flux')
        pass

    return model


# Create context-specific model based on transcript distribution
def contextualize(model, binning_dict, new_name=False):
    
    # generate reaction bins based on transcription
    print('Partitioning genes/reactions by transcript abundance...')
    ignore, exclude, perc_top, perc_hi, perc_mid, perc_lo = parse_reaction_binning(model, binning_dict)
        
    # Identify those reactions that are to be pruned from each bin
    print('Generating contextualized model...')
    contextualized_model = copy.deepcopy(model)
    
    if len(ignore) > 0: 
        #print('Ignoring ' + str(len(ignore)) + ' context-specific reactions defined by user.')
        pass
    
    if len(exclude) > 0: 
        #print('Pruning ' + str(len(exclude)) + ' context-specific reactions defined by user.')
        contextualized_model = prune_and_test(contextualized_model, exclude)
    
    remove_lo = pFBA_by_percent_of_optimum(contextualized_model, perc_lo, optimum_fraction=0.01, exclude_from_min=False)
    contextualized_model = prune_and_test(contextualized_model, remove_lo)

    remove_mid = pFBA_by_percent_of_optimum(contextualized_model, perc_mid, optimum_fraction=0.99, exclude_from_min=False)
    contextualized_model = prune_and_test(contextualized_model, remove_mid)

    remove_hi = pFBA_by_percent_of_optimum(contextualized_model, perc_hi, optimum_fraction=0.01)
    contextualized_model = prune_and_test(contextualized_model, remove_hi)
    
    remove_top = pFBA_by_percent_of_optimum(contextualized_model, perc_top, optimum_fraction=0.99)
    contextualized_model = prune_and_test(contextualized_model, remove_top)
    
    removed = set().union(exclude, remove_lo, remove_mid, remove_hi, remove_top)
    print('Pruned ' + str(len(removed)) + '/'  + str(len(list(model.reactions))) + ' reactions during contextualization.')
    
    contextualized_model.id = str(contextualized_model.id) + '_dante'
    if new_name != False:
        contextualized_model.name = new_name
    
    return contextualized_model

