from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import GAllele

import io
import json
import imp
import pprint
import warnings
import math
from numpy import *

imp.load_source('ols', '../ols.py')
from ols import ols

class Metabolite:
    keggID = 0
    props = {}

    def __init__(self, theKeggID, theProps):
        self.keggID = theKeggID
        self.props = theProps

class Disambiguator:
    ambiguities = {}
    keggIDToAmbiguityID = {}
    genome = None
    mlrPropCombo = ['PUBCHEM_EFFECTIVE_ROTOR_COUNT', '3DMET_ELECTROSTATIC_ENERGY', '3DMET_DENSITY', 'PUBCHEM_COMPLEXITY', '3DMET_HBOND_ACCEPTOR', '3DMET_ANGLE_BEND_ENERGY', '3DMET_BASIC_ATOMS', '3DMET_NONBOND_ENERGY']
    #mlrPropCombo = ['PUBCHEM_XLOGP', 'CHEMSPIDER_HBONDACCEPTORS', '3DMET_SINGLE_BONDS', '3DMET_ACIDIC_ATOMS']
    generationsToEvolve = 5000
    ga = None

    def __init__(self):
        ambiguitiesPropsFile = open('ambiguities.json', 'r')
        ambiguitiesPropsJSON = ambiguitiesPropsFile.read()
        self.ambiguities = json.loads(ambiguitiesPropsJSON)

        #each allele selects from one of the ambiguous metabolites with the same weight
        setOfAlleles = GAllele.GAlleles()
        alleleCount = 0
        for ambiguityID, ambiguityProps in self.ambiguities.iteritems():
            scanID = ambiguityProps["scanid"]
            metabolites = ambiguityProps["candidates"]
            alleleArray = []

            for keggID, props in metabolites.iteritems():
                #this is super hackish, but it works
                #for each metabolite candidate, we set the ambiguity's scan id as a property on the metabolite candidate property list itself
                #that way, we can know the ambiguity's scan id without having to know the ambiguityid
                props["SUSPECTED_SCANTIME"] = int(scanID)
                metabolite = Metabolite(keggID, props)
                self.keggIDToAmbiguityID[keggID] = ambiguityID
                alleleArray.append(metabolite)

            #add a blank metabolite without any properties to randomly switch off this allele
            repressedAllele = Metabolite(0, {})
            alleleArray.append(repressedAllele)

            alleleList = GAllele.GAlleleList(alleleArray)
            setOfAlleles.add(alleleList)
            alleleCount += 1

        genome = G1DList.G1DList(alleleCount)
        genome.setParams(allele=setOfAlleles)

        # The evaluator function (objective function)
        genome.evaluator.set(self.evaluateScore)
        genome.mutator.set(Mutators.G1DListMutatorAllele)
        genome.initializator.set(Initializators.G1DListInitializatorAllele)
        
        # Genetic Algorithm Instance
        self.ga = GSimpleGA.GSimpleGA(genome)
        self.ga.selector.set(Selectors.GRouletteWheel)
        self.ga.setGenerations(self.generationsToEvolve)

        self.ga.evolve(freq_stats=50)

    def evaluateScore(self, chromosome):
        xMatrix = []
        yVector = []

        for metabolite in chromosome:
            knownProps = metabolite.props

            #blank, filler metabolites wont have a suspected scantime
            if 'SUSPECTED_SCANTIME' in knownProps:
                scanTime = knownProps['SUSPECTED_SCANTIME']
                xMatrixRow = []
                countThisMetabolite = True #those without the full set of properties wont be counted
                #note: we use this same mechanism for canceling out metabolites if it would be be beneficial to do so
                for prop in self.mlrPropCombo:
                    if prop in knownProps:
                        val = knownProps[prop]
                        xMatrixRow.append(val)
                    else:
                        #return False
                        countThisMetabolite = False

                #all properties extant and added to matrix row
                if countThisMetabolite == True:
                    xMatrix.append(xMatrixRow)
                    yVector.append(scanTime)

        try:
            m = ols(array(yVector), array(xMatrix))
        except:
            return 0

        rSquared = m.R2
        return rSquared

    def printSummary(self):
        bestIndividual = disambiguator.ga.bestIndividual()
        xMatrix = []
        yVector = []
        chosenKeggIDs = {}

        print("best individual's keggids:")
        for metabolite in bestIndividual:
            knownProps = metabolite.props
            keggID = metabolite.keggID
            print(keggID)

            #blank, filler metabolites wont have a suspected scantime
            if 'SUSPECTED_SCANTIME' in knownProps:
                scanTime = knownProps['SUSPECTED_SCANTIME']
                xMatrixRow = []
                countThisMetabolite = True #those without the full set of properties wont be counted
                #note: we use this same mechanism for canceling out metabolites if it would be be beneficial to do so
                for prop in self.mlrPropCombo:
                    if prop in knownProps:
                        val = knownProps[prop]
                        xMatrixRow.append(val)
                    else:
                        #return False
                        countThisMetabolite = False

                #all properties extant and added to matrix row
                if countThisMetabolite == True:
                    xMatrix.append(xMatrixRow)
                    yVector.append(scanTime)
                    chosenKeggIDs[keggID] = scanTime


        try:
            m = ols(array(yVector), array(xMatrix))
        except:
            return 0

        m = ols(array(yVector), array(xMatrix))

        b = m.b
        summary = {}


        print("")
        print("summary of all ambiguous metabolites:")
        for ambiguityID, ambiguityProps in self.ambiguities.iteritems():
            metabolites = ambiguityProps["candidates"]

            for keggID, knownProps in metabolites.iteritems():
                addToSummary = True
                scanTime = knownProps['SUSPECTED_SCANTIME']
                lookedUpPropArr = []
                for prop in self.mlrPropCombo:
                    if prop in knownProps:
                        val = knownProps[prop]
                        lookedUpPropArr.append(val)
                    else:
                        addToSummary = False
                        break
                if addToSummary:
                    yPred = b[0]
                    for propIndex in range(0, len(lookedUpPropArr)):
                        propVal = lookedUpPropArr[propIndex]
                        propCoefficient = b[propIndex + 1]
                        yPred += propCoefficient * propVal

                    metaboliteSummary = {
                        "scan": scanTime,
                        "prediction": yPred,
                        "error": (math.fabs(scanTime - yPred) / scanTime)
                    }
                    if keggID in chosenKeggIDs and chosenKeggIDs[keggID] == scanTime:
                        metaboliteSummary["chosen"] = True

                    summaryKey = "ambiguity" + str(ambiguityID)
                    if summaryKey not in summary:
                        summary[summaryKey] = []

                    summary[summaryKey].append(metaboliteSummary)


        pp = pprint.PrettyPrinter()
        pp.pprint(summary)

#sometimes scipy generates warnings, which usually means something went wrong and we might get bad data
#to remedy this, switch all warnings to error, catch them when doing the multiple linear regression, and disregard that result
warnings.resetwarnings()
warnings.simplefilter('error')

disambiguator = Disambiguator()
disambiguator.printSummary()
