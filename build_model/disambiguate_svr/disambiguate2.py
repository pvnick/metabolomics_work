import io
import json
import imp
import pprint
import warnings
import math
from numpy import *
from sklearn.svm import SVR
import pylab as pl

imp.load_source('ols', '../ols.py')
from ols import ols

class MetaboliteCandidate:
    keggID = 0
    props = {}

    def __init__(self, theKeggID, theProps):
        self.keggID = theKeggID
        self.props = theProps

class Disambiguator:
    model = None
    svr_rbf = None
    xMatrix = []
    yVector = []
    inUseCandidates = []
    ambiguities = {}
    keggIDToAmbiguityID = {}
    m = None
    maxScanIDPredictionError = 0.05
    mlrPropCombo = ['PUBCHEM_HBOND_ACCEPTOR', 'PUBCHEM_HEAVY_ATOM_COUNT', 'PUBCHEM_XLOGP']
    #mlrPropCombo = ["PUBCHEM_HBOND_DONOR","PUBCHEM_COMPLEXITY","PUBCHEM_TPSA"]
    finalSampleSize = 0

    def __init__(self):
        self.svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

        ambiguitiesPropsFile = open('ambiguities.json', 'r')
        ambiguitiesPropsJSON = ambiguitiesPropsFile.read()
        rawAmbiguities = json.loads(ambiguitiesPropsJSON)

        for ambiguityID, ambiguityProps in rawAmbiguities.iteritems():
            scanID = ambiguityProps["scanid"]
            metabolites = ambiguityProps["candidates"]
            confident = ambiguityProps["confident"]

            if ambiguityID not in self.ambiguities:
                self.ambiguities[ambiguityID] = {
                    "scanID": scanID,
                    "candidates": {},
                    "confident": confident
                } 

            for keggID, props in metabolites.iteritems():
                #this is super hackish, but it works
                #for each metabolite candidate, we set the ambiguity's scan id as a property on the metabolite candidate property list itself
                #that way, we can know the ambiguity's scan id without having to know the ambiguityid
                props["SUSPECTED_SCANTIME"] = float(scanID)
                metabolite = MetaboliteCandidate(keggID, props)
                self.keggIDToAmbiguityID[keggID] = ambiguityID
                self.ambiguities[ambiguityID]["candidates"][keggID] = metabolite

    def disambiguate(self):
        self.reset()
        #first build a model for masses with only a single candidate
        self.addAllConfidentCandidates()
        self.model = self.svr_rbf.fit(self.xMatrix, self.yVector)
        self.addAllNonconfidentCandidates()

        self.removeHighErrorCandidates()

        return len(self.inUseCandidates)

    def tryMLR(self):
        try:
            self.m = ols(array(self.yVector), array(self.xMatrix)) #, y_varnm = 'y', x_varnm = ['x1','x2','x3','x4','x5','x6','x7'])
            #self.m.summary()
            return True
        except:
            #print("error")
            return False

    def addAllConfidentCandidates(self):
        for ambiguityID, ambiguityProps in self.ambiguities.iteritems():
            candidates = ambiguityProps["candidates"]
            isConfident = int(ambiguityProps["confident"])
            if isConfident == 1:
                candidate = candidates.itervalues().next()
                self.tryToAddMetabolite(candidate)

    def addAllNonconfidentCandidates(self):
        for ambiguityID, ambiguityProps in self.ambiguities.iteritems():
            candidates = ambiguityProps["candidates"]
            isConfident = int(ambiguityProps["confident"])
            if isConfident == 0:
                #choose the candidate whose elution time is closest to the predicted time
                closestCandidate = None
                smallestError = inf

                for candidate in candidates.itervalues():

                    validCandidate = True
                    props = candidate.props
                    scanID = props["SUSPECTED_SCANTIME"]
                    lookedUpPropArr = []
                    for prop in self.mlrPropCombo:
                        if prop in props:
                            val = props[prop]
                            lookedUpPropArr.append(val)
                        else:
                            validCandidate = False
                            break

                    if validCandidate:
                        predScanID = self.model.predict([lookedUpPropArr])
                        rawError = fabs(predScanID - scanID)

                        if closestCandidate == None or rawError < smallestError:
                            closestCandidate = candidate
                            smallestError = rawError
                
                if closestCandidate != None:
                    self.tryToAddMetabolite(candidate)

    def removeHighErrorCandidates(self):
        quantity = len(self.inUseCandidates)
        i = 0
        while i < quantity:
            candidate = self.inUseCandidates[i]
            validCandidate = True
            props = candidate.props
            scanID = props["SUSPECTED_SCANTIME"]
            lookedUpPropArr = []
            for prop in self.mlrPropCombo:
                if prop in props:
                    val = props[prop]
                    lookedUpPropArr.append(val)
                else:
                    validCandidate = False
                    del self.inUseCandidates[i]
                    del self.yVector[i]
                    del self.xMatrix[i]
                    quantity -= 1
                    i -= 1
                    break

            if validCandidate:
                predScanID = self.model.predict([lookedUpPropArr])
            
                errorPct = fabs(predScanID - scanID) / float(scanID)
                if errorPct > self.maxScanIDPredictionError:
                    del self.inUseCandidates[i]
                    del self.yVector[i]
                    del self.xMatrix[i]
                    quantity -= 1
                    i -= 1

            i += 1

    def tryToAddMetabolite(self, metabolite):
        #returns true if added, false if one or more properties were not found

        if not isinstance(metabolite, MetaboliteCandidate):
            return False

        knownProps = metabolite.props
        scanTime = knownProps['SUSPECTED_SCANTIME']
        xMatrixRow = []
        for prop in self.mlrPropCombo:
            if prop in knownProps:
                val = knownProps[prop]
                xMatrixRow.append(val)
            else:
                return False
        #all properties extant and added to matrix row
        self.inUseCandidates.append(metabolite)
        self.xMatrix.append(xMatrixRow)
        self.yVector.append(scanTime)
        return True


    def reset(self):
        self.inUseCandidates = []
        self.xMatrix = []
        self.yVector = []

    def printSummary(self):
        self.tryMLR()

        b = self.m.b
        summary = {}

        print("")
        print("summary of all ambiguous metabolites:")
        for ambiguityID, ambiguityProps in self.ambiguities.iteritems():
            candidates = ambiguityProps["candidates"]

            for keggID, candidate in candidates.iteritems():
                addToSummary = True
                knownProps = candidate.props
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
                        "keggid": keggID,
                        "scan": scanTime,
                        "prediction": yPred,
                        "error": (math.fabs(scanTime - yPred) / scanTime)
                    }
                    if candidate in self.inUseCandidates:
                        metaboliteSummary["chosen"] = True

                    summaryKey = "ambiguity" + str(ambiguityID)
                    if summaryKey not in summary:
                        summary[summaryKey] = []

                    summary[summaryKey].append(metaboliteSummary)


        pp = pprint.PrettyPrinter()
        pp.pprint(summary)

#sometimes scipy generates warnings, which usually means something went wrong and we might get bad data
#to remedy this, switch all warnings to error, catch them when doing the multiple linear regression, and disregard that result
#warnings.resetwarnings()
#warnings.simplefilter('error')

if __name__ == '__main__':
    disambiguator = Disambiguator()
    sampleSize = disambiguator.disambiguate()
#disambiguator.printSummary()
