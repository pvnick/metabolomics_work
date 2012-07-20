import io
import json
import imp
import pprint
import warnings
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
    mlrPropCombo = ["PUBCHEM_XLOGP", "3DMET_DENSITY", "3DMET_ANGLE_BEND_ENERGY"]
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
            for keggID  in metabolites.iterkeys():
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

        pp = pprint.PrettyPrinter()
        pp.pprint(self.xMatrix)

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
        self.yVector.append(keggID)
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
        self.yVector.append(keggID)
        return True
        
disambiguator = Disambiguator()
disambiguator.doTrial()
