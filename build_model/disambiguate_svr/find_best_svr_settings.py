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

GENERATIONS_TO_EVOLVE = 1000

disambiguator = Disambiguator()

def evaluateScore(chromosome):
    disambiguator.reset()
    disambiguator.svr_C = chromosome[0]
    disambiguator.svr_gamma = chromosome[1]
    return disambiguator.disambiguate()

setOfAlleles = GAllele.GAlleles()
alleleArray = []
for i in range(-15, 15):
    alleleArray.append(2**i)
alleleList = GAllele.GAlleleList(alleleArray)
setOfAlleles.add(alleleList)

alleleArray = []
for i in range(-15, 15):
    alleleArray.append(2**i)
alleleList = GAllele.GAlleleList(alleleArray)
setOfAlleles.add(alleleList)

genome = G1DList.G1DList(2)
genome.setParams(allele=setOfAlleles)

# The evaluator function (objective function)
genome.evaluator.set(evaluateScore)
genome.mutator.set(Mutators.G1DListMutatorAllele)
genome.crossover.set(Crossovers.G1DListCrossoverSinglePoint)
genome.initializator.set(Initializators.G1DListInitializatorAllele)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setGenerations(GENERATIONS_TO_EVOLVE)

ga.evolve(freq_stats=1)

bestIndividual = ga.bestIndividual()
print(bestIndividual)

