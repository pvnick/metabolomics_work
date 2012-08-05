from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Crossovers
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import GAllele

import io
import json
import imp
import pprint
import warnings
from numpy import *

imp.load_source('ols', '../ols.py')
from ols import ols

from disambiguate import Disambiguator

PROP_COUNT = 5
GENERATIONS_TO_EVOLVE = 1000

disambiguator = Disambiguator()

#uniqueProps = ["CHEMSPIDER_ACDBCFPH55","CHEMSPIDER_ACDBCFPH74","CHEMSPIDER_ACDKOCPH55","CHEMSPIDER_ACDKOCPH74","CHEMSPIDER_ACDLOGDPH55","CHEMSPIDER_ACDLOGDPH74","CHEMSPIDER_ACDLOGP","CHEMSPIDER_BOILINGPOINT","CHEMSPIDER_DENSITY","CHEMSPIDER_ENTHALPYOFVAPORIZATION","CHEMSPIDER_FLASHPOINT","CHEMSPIDER_FREELYROTATINGBONDS","CHEMSPIDER_HBONDACCEPTORS","CHEMSPIDER_HBONDDONORS","CHEMSPIDER_INDEXOFREFRACTION","CHEMSPIDER_MOLARREFRACTIVITY","CHEMSPIDER_MOLARVOLUME","CHEMSPIDER_OFRULEOF5VIOLATIONS","CHEMSPIDER_POLARIZABILITY","CHEMSPIDER_POLARSURFACEAREA","CHEMSPIDER_SURFACETENSION","CHEMSPIDER_VAPOURPRESSURE","PUBCHEM_COMPLEXITY","PUBCHEM_CONFORMER_SAMPLING_RMSD","PUBCHEM_COVALENTLY_BONDED_UNIT_COUNT","PUBCHEM_DEFINED_ATOM_ATEREOCENTER_COUNT","PUBCHEM_DEFINED_BOND_STEREOCENTER_COUNT","PUBCHEM_EFFECTIVE_ROTOR_COUNT","PUBCHEM_EXACT_MASS","PUBCHEM_FEATURE_3D_ACCEPTOR_COUNT","PUBCHEM_FEATURE_3D_ANION_COUNT","PUBCHEM_FORMAL_CHARGE","PUBCHEM_HBOND_ACCEPTOR","PUBCHEM_HBOND_DONOR","PUBCHEM_HEAVY_ATOM_COUNT","PUBCHEM_ISOTOPE_ATOM_COUNT","PUBCHEM_MOLECULAR_WEIGHT","PUBCHEM_MONOISOTOPIC_MASS","PUBCHEM_TPSA","PUBCHEM_UNDEFINED_ATOM_STEREOCENTER_COUNT","PUBCHEM_UNDEFINED_BOND_STEREOCENTER_COUNT","PUBCHEM_XLOGP"];
uniqueProps = ["3DMET_ACIDIC_ATOMS","3DMET_ANGLE_BEND_ENERGY","3DMET_AROMATIC_ATOMS","3DMET_AROMATIC_BONDS","3DMET_ASA","3DMET_BASIC_ATOMS","3DMET_BOND_STRETCHBEND_ENERGY","3DMET_CHIRAL_ATOMS","3DMET_DENSITY","3DMET_DIAMETER","3DMET_DIPOLE","3DMET_DOUBLE_BONDS","3DMET_ELECTROSTATIC_ENERGY","3DMET_FORMAL_CHARGE","3DMET_GLOBULARITY","3DMET_HBOND_ACCEPTOR","3DMET_HBOND_DONOR","3DMET_HEAVY_ATOMS","3DMET_LOGP_O_TO_W","3DMET_NONBOND_ENERGY","3DMET_NUMBER_OF_ATOMS","3DMET_NUMBER_OF_BONDS","3DMET_NUMBER_OF_RINGS","3DMET_OUTOFPLANE_ENERGY","3DMET_POTENTIAL_ENERGY","3DMET_ROTATABLE_SINGLE_BONDS","3DMET_SINGLE_BONDS","3DMET_SLOGP","3DMET_SMR","3DMET_SOLVATION_ENERGY","3DMET_TORSION_ENERGY","3DMET_TPSA","3DMET_TRIPLE_BONDS","3DMET_VAN_DEL_WAALS_ENERGY","3DMET_VOLUME","3DMET_VSA","3DMET_WEIGHT","CHEMSPIDER_ACDBCFPH55","CHEMSPIDER_ACDBCFPH74","CHEMSPIDER_ACDKOCPH55","CHEMSPIDER_ACDKOCPH74","CHEMSPIDER_ACDLOGDPH55","CHEMSPIDER_ACDLOGDPH74","CHEMSPIDER_ACDLOGP","CHEMSPIDER_BOILINGPOINT","CHEMSPIDER_DENSITY","CHEMSPIDER_ENTHALPYOFVAPORIZATION","CHEMSPIDER_FLASHPOINT","CHEMSPIDER_FREELYROTATINGBONDS","CHEMSPIDER_HBONDACCEPTORS","CHEMSPIDER_HBONDDONORS","CHEMSPIDER_INDEXOFREFRACTION","CHEMSPIDER_MOLARREFRACTIVITY","CHEMSPIDER_MOLARVOLUME","CHEMSPIDER_OFRULEOF5VIOLATIONS","CHEMSPIDER_POLARIZABILITY","CHEMSPIDER_POLARSURFACEAREA","CHEMSPIDER_SURFACETENSION","CHEMSPIDER_VAPOURPRESSURE","PUBCHEM_COMPLEXITY","PUBCHEM_CONFORMER_SAMPLING_RMSD","PUBCHEM_COVALENTLY_BONDED_UNIT_COUNT","PUBCHEM_DEFINED_ATOM_ATEREOCENTER_COUNT","PUBCHEM_DEFINED_BOND_STEREOCENTER_COUNT","PUBCHEM_EFFECTIVE_ROTOR_COUNT","PUBCHEM_EXACT_MASS","PUBCHEM_FEATURE_3D_ACCEPTOR_COUNT","PUBCHEM_FEATURE_3D_ANION_COUNT","PUBCHEM_FORMAL_CHARGE","PUBCHEM_HBOND_ACCEPTOR","PUBCHEM_HBOND_DONOR","PUBCHEM_HEAVY_ATOM_COUNT","PUBCHEM_ISOTOPE_ATOM_COUNT","PUBCHEM_MOLECULAR_WEIGHT","PUBCHEM_MONOISOTOPIC_MASS","PUBCHEM_TPSA","PUBCHEM_UNDEFINED_ATOM_STEREOCENTER_COUNT","PUBCHEM_UNDEFINED_BOND_STEREOCENTER_COUNT","PUBCHEM_XLOGP","CALCULATED_ASA"];

def evaluateScore(chromosome):
    disambiguator.reset()
    disambiguator.mlrPropCombo = chromosome 
    return disambiguator.disambiguate()

setOfAlleles = GAllele.GAlleles()
for i in range(PROP_COUNT):
    alleleList = GAllele.GAlleleList(uniqueProps)
    setOfAlleles.add(alleleList)

genome = G1DList.G1DList(PROP_COUNT)
genome.setParams(allele=setOfAlleles)

# The evaluator function (objective function)
genome.evaluator.set(evaluateScore)
genome.mutator.set(Mutators.G1DListMutatorAllele)
genome.crossover.set(Crossovers.G1DListCrossoverTwoPoint)
genome.initializator.set(Initializators.G1DListInitializatorAllele)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setGenerations(GENERATIONS_TO_EVOLVE)

ga.evolve(freq_stats=1)

bestIndividual = ga.bestIndividual()
print(bestIndividual)
