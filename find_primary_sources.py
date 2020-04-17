#!/usr/bin/env python3

import cobra
import numpy

# Scale each active exchange back and examine its influence on objective flux
def find_primary_sources(model, flux_samples=False, fraction=0.01, top=3):
    # Requires a model 
    # Optional: flux_samples = flux samples pandas dataframe associated with model
    #           fraction = percent of median flux to limit exchange reactions by
    #           top = number of carbon and nitrogen sources to print in report

    sources = {}
    c_sources = []
    n_sources = []
    p_source = ['p_source', -1.0]
    s_source = ['s_source', -1.0]
    solution = model.optimize()
    objVal = solution.objective_value
    
    # Parse exchange flux samples for imported metabolites
    exchanges = [rxn.id for rxn in model.boundary]
    for rxn in exchanges:
        if isinstance(flux_samples, pandas.DataFrame):
            flux = numpy.median(flux_samples[rxn])
            flux_lower = numpy.quantile(flux_samples[rxn], 0.25) * fraction
            flux_upper = numpy.quantile(flux_samples[rxn], 0.75) * fraction
        else:
            flux = solution.fluxes[rxn]
            flux_lower = -abs(solution.fluxes[rxn]) * fraction
            flux_upper = abs(solution.fluxes[rxn]) * fraction
        if flux >= -1e-6: continue # Skip exported byproducts or unused reactions
        
        # Test for disproportionate effect on objective
        old_bounds = model.reactions.get_by_id(rxn).bounds
        model.reactions.get_by_id(rxn).bounds = (flux_lower, flux_upper)        
        new_objVal = model.slim_optimize()
        model.reactions.get_by_id(rxn).bounds = old_bounds # Reset bounds
        if str(new_objVal) == 'nan': new_objVal = objVal * fraction # Correct for nan
        
        # Calculate the degree of change to objective value
        if new_objVal != objVal:
            corrected_flux = abs(flux) / (new_objVal / objVal)
        else:
            corrected_flux = 1.
            
        metabolite = model.reactions.get_by_id(rxn).reactants[0]
        sources[metabolite.id] = {}
            
        # Normalize elemental component contributions
        for element in metabolite.elements.keys():
            element_supply = float(metabolite.elements[element]) * corrected_flux
            if element_supply > 0.: element_supply = numpy.log(element_supply)
            sources[metabolite.id][element] = element_supply
                
            # Identify largest sources of main elements
            if element == 'C' and element_supply > 0.0:
                c_sources.append([metabolite.id, element_supply])
            elif element == 'N' and element_supply > 0.0:
                n_sources.append([metabolite.id, element_supply])
            elif element == 'P' and element_supply > 0.0:
                p_source = [metabolite.id, element_supply]
            elif element == 'S' and element_supply > 0.0:
                s_source = [metabolite.id, element_supply]
    
    # Rank by largest contributions
    def getKey(item): return item[1]
    c_sources = sorted(c_sources, reverse=True, key=getKey)
    n_sources = sorted(n_sources, reverse=True, key=getKey)
    
    print('Top carbon sources:')
    if top > len(c_sources): top = len(c_sources)
    for x in range(0, top):
        print(str(x+1) + '. ' + model.metabolites.get_by_id(c_sources[x][0]).name + ' (' + str(round(c_sources[x][1],3)) + ')')

    print('\nTop nitrogen sources:')
    if top > len(n_sources): top = len(n_sources)
    for x in range(0, top):
        print(str(x+1) + '. ' + model.metabolites.get_by_id(n_sources[x][0]).name + ' (' + str(round(n_sources[x][1],3)) + ')')

    print('\nPrimary phosphorous source:')
    print(model.metabolites.get_by_id(p_source[0]).name + ' (' + str(round(p_source[1],3)) + ')')
    
    print('\nPrimary sulfur source:')
    print(model.metabolites.get_by_id(s_source[0]).name + ' (' + str(round(s_source[1],3)) + ')')
    
    return sources
