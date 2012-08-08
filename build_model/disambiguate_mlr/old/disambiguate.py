import io
import json
import imp
import pprint
import warnings
import math
from numpy import *

imp.load_source('ols', '../ols.py')
from ols import ols

class Disambiguator:
    xMatrix = []
    yVector = []
    knowns = {}
    ambiguities = {}
    keggIDToAmbiguityID = {}
    highestRSquared = 0
    mlrPropCombo = ["PUBCHEM_XLOGP", "3DMET_DENSITY", "3DMET_ANGLE_BEND_ENERGY", "3DMET_ACIDIC_ATOMS", "CHEMSPIDER_HBONDDONORS", "CHEMSPIDER_HBONDACCEPTORS", "3DMET_SINGLE_BONDS", "CHEMSPIDER_ACDLOGDPH55", "CHEMSPIDER_ACDLOGDPH74"]
    #mlrPropCombo = ['PUBCHEM_XLOGP', 'CHEMSPIDER_HBONDACCEPTORS', '3DMET_SINGLE_BONDS', '3DMET_ACIDIC_ATOMS']
    ambiguousKeggIDsInUse = {} #ambiguityid: current_keggid_from_list

    def __init__(self):
        ambiguitiesPropsFile = open('ambiguities.json', 'r')
        ambiguitiesPropsJSON = ambiguitiesPropsFile.read()
        self.ambiguities = json.loads(ambiguitiesPropsJSON)

        knownsPropsFile = open('knowns.json', 'r')
        knownsPropsJSON = knownsPropsFile.read()
        self.knowns = json.loads(knownsPropsJSON)

        for ambiguityID, metabolites in self.ambiguities.iteritems():
            minKeggID = None
            minKeggIDNumericPart = inf #all keggids are lower than infinity!
            for keggID in metabolites.iterkeys():
                self.keggIDToAmbiguityID[keggID] = ambiguityID

                #our initial trial uses the metabolites with the lowest kegg id
                #the assumption is that those are more common and therefore more likely to be correct
                keggIDNumericPart = int(keggID[1:])
                if keggIDNumericPart < minKeggIDNumericPart:
                    minKeggID = keggID
                    minKeggIDNumericPart = keggIDNumericPart
            if minKeggIDNumericPart < inf:
                self.ambiguousKeggIDsInUse[ambiguityID] = minKeggID

    def doTrial(self):
        self.reset()
        self.addAllKnownMetabolites()
        self.addAllInUseAmbiguousMetabolites()
#todo: dont compare if model improved, instead just choose all metabolites that are as close to the line as possible
        didModelImprove = self.compareNewRSquared()

    def tryAllAmbiguousMetabolites(self):
        #returns true if the model improved and false if it stayed the same
        #this method should be called continously until the model doesnt improve anymore
        originalHighestRSquared = self.highestRSquared
        for ambiguityID, metabolites in self.ambiguities.iteritems():
            for keggID in metabolites.iterkeys():
                oldKeggID = self.ambiguousKeggIDsInUse[ambiguityID]
                self.ambiguousKeggIDsInUse[ambiguityID] = keggID
                didModelImprove = self.doTrial()
                if not didModelImprove:
                    self.ambiguousKeggIDsInUse[ambiguityID] = oldKeggID

        newHighestRSquared = self.highestRSquared
        return newHighestRSquared > originalHighestRSquared

    def compareNewRSquared(self):
        rSquared = self.getCurrentRSquared()
        if rSquared > self.highestRSquared:
            self.highestRSquared = rSquared
            return True
        else:
            return False

    def getCurrentRSquared(self):
        try:
            m = ols(array(self.yVector), array(self.xMatrix))
        except:
            return 0

        rSquared = m.R2
        return rSquared

    def reset(self):
        self.xMatrix = []
        self.yVector = []

    def addAllInUseAmbiguousMetabolites(self):
        for keggID in self.ambiguousKeggIDsInUse.itervalues():
            self.addPropsFromAmbiguousKeggID(keggID)

    def addAllKnownMetabolites(self):
        for keggID, props in self.knowns.iteritems():
            self.addPropsFromUnambiguousKeggID(keggID)

    def addPropsFromUnambiguousKeggID(self, keggID):
        #returns true if added, false if one or more properties were not found
        if keggID not in self.knowns:
            return False
        knownProps = self.knowns[keggID]

        if isinstance(knownProps, dict) == False:
            return False
        
        scanTime = knownProps['MEASURED_SCANTIME']
        xMatrixRow = []
        for prop in self.mlrPropCombo:
            if prop in knownProps:
                val = knownProps[prop]
                xMatrixRow.append(val)
            else:
                return False
        #all properties extant and added to matrix row
        self.xMatrix.append(xMatrixRow)
        self.yVector.append(scanTime)
        return True

    def addPropsFromAmbiguousKeggID(self, keggID):
        #returns true if added, false if one or more properties were not found
        if keggID not in self.keggIDToAmbiguityID:
            return False
        ambiguityID = self.keggIDToAmbiguityID[keggID]
        knownProps = self.ambiguities[ambiguityID][keggID]
        scanTime = knownProps['SUSPECTED_SCANTIME']
        xMatrixRow = []
        for prop in self.mlrPropCombo:
            if prop in knownProps:
                val = knownProps[prop]
                xMatrixRow.append(val)
            else:
                return False
        #all properties extant and added to matrix row
        self.xMatrix.append(xMatrixRow)
        self.yVector.append(scanTime)
        return True
    
    def buildModel(self):
        while (self.tryAllAmbiguousMetabolites()):
            print(self.highestRSquared)

        self.printSummary()

    def printSummary(self):
        self.doTrial()
        m = ols(array(self.yVector), array(self.xMatrix))
        #m.summary()

        b = m.b
        summary = {}

        for keggID, knownProps in self.knowns.iteritems():
            addToSummary = True
            scanTime = int(knownProps['MEASURED_SCANTIME'])
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

                summary["unambiguous_" + str(keggID)] = metaboliteSummary

        for ambiguityID, metabolites in self.ambiguities.iteritems():
            for keggID, knownProps in metabolites.iteritems():
                addToSummary = True
                scanTime = int(knownProps['SUSPECTED_SCANTIME'])
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
                    if self.ambiguousKeggIDsInUse[ambiguityID] == keggID:
                        metaboliteSummary["chosen"] = True

                    summaryKey = "ambiguity" + str(ambiguityID)
                    if summaryKey not in summary:
                        summary[summaryKey] = []

                    summary[summaryKey].append(metaboliteSummary)


        pp = pprint.PrettyPrinter()
        pp.pprint(summary)
                

        #for ambiguityID, metabolites in self.ambiguities.iteritems():
        #    for keggID in metabolites.iterkeys():
        #for ambiguityID, metabolites in self.ambiguities.iteritems():
        #    for keggID in metabolites.iterkeys():

        

#sometimes scipy generates warnings, which usually means something went wrong and we might get bad data
#to remedy this, switch all warnings to error, catch them when doing the multiple linear regression, and disregard that result
warnings.resetwarnings()
warnings.simplefilter('error')
        
disambiguator = Disambiguator()

disambiguator.buildModel()
print(len(disambiguator.yVector))
