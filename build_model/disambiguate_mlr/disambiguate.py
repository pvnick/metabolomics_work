import io
import json
import imp
import pprint
import warnings
import math
from numpy import *
import pylab as pl

imp.load_source('ols', '../ols.py')
nameresolver = imp.load_source('nameresolver', '../get_keggid_name.py')
from ols import ols

class MetaboliteCandidate:
    keggID = 0
    props = {}

    def __init__(self, theKeggID, theProps):
        self.keggID = theKeggID
        self.props = theProps

class Disambiguator:
    xMatrix = []
    yVector = []
    inUseCandidates = []
    ambiguities = {}
    keggIDToAmbiguityID = {}
    m = None
    maxScanIDPredictionError = 0.25
    mlrPropCombo = ['PUBCHEM_EFFECTIVE_ROTOR_COUNT', 'CHEMSPIDER_ACDBCFPH55', 'CHEMSPIDER_ACDKOCPH55', 'CHEMSPIDER_MOLARVOLUME', 'PUBCHEM_MONOISOTOPIC_MASS', 'CHEMSPIDER_ACDBCFPH74', 'CHEMSPIDER_ACDKOCPH74', 'CHEMSPIDER_FLASHPOINT', 'CHEMSPIDER_ENTHALPYOFVAPORIZATION', 'PUBCHEM_UNDEFINED_ATOM_STEREOCENTER_COUNT', 'CHEMSPIDER_OFRULEOF5VIOLATIONS', 'CALCULATED_ASA', 'CHEMSPIDER_ACDLOGDPH55', 'CHEMSPIDER_ACDLOGDPH74', 'LOGP_BEST_GUESS', 'PUBCHEM_HBOND_ACCEPTOR', 'PUBCHEM_HBOND_DONOR']
    #mlrPropCombo = ['CHEMSPIDER_POLARSURFACEAREA', 'CHEMSPIDER_ACDKOCPH55', 'PUBCHEM_MONOISOTOPIC_MASS', 'CHEMSPIDER_HBONDACCEPTORS', 'CHEMSPIDER_OFRULEOF5VIOLATIONS']
    #mlrPropCombo = ['PUBCHEM_XLOGP', 'CALCULATED_ASA']
    finalSampleSize = 0

    def __init__(self):
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

    def makePredictionVector(self):
        b = self.m.b
        predVector = []
        for xMatrixRow in self.xMatrix:
            yPred = b[0]
            for i in range(1, len(b)):
                yPred += xMatrixRow[i-1] * b[i]
            predVector.append(yPred)

        return predVector

    def checkFitness(self):
        self.reset()
        #first build a model for masses with only a single candidate
        self.addAllConfidentCandidates()
        if self.tryMLR():
            rSquared = self.m.R2
            self.removeHighErrorCandidates()

            filteredConfidentCandidateCount = len(self.inUseCandidates)
            if filteredConfidentCandidateCount < 35:
                return 0
            if rSquared < 0: 
                return 0
            return rSquared

            self.addAllNonconfidentCandidates()
            self.removeHighErrorCandidates()

            #model score. gives precedence to the total number of valid candidates followed by confident ones
            return len(self.inUseCandidates) * 1000 + filteredConfidentCandidateCount

        return 0

    def disambiguate(self):
        #todo: this should be broken into two functions, one for actual disambiguation and one for the genetic algorithm to call
        self.reset()
        #first build a model for masses with only a single candidate
        self.addAllConfidentCandidates()
        if self.tryMLR():
            yPred = self.makePredictionVector()
            pl.scatter(self.yVector, yPred, c='red', label='raw, confident')
            pl.hold('on')

            rSquared = self.m.R2
            self.removeHighErrorCandidates()

            yPred = self.makePredictionVector()
            self.m.summary()
            pl.scatter(self.yVector, yPred, c='green', label='filtered, confident')

            self.addAllNonconfidentCandidates()
            self.m.summary()
            

            
            yPred = self.makePredictionVector()
            pl.scatter(self.yVector, yPred, c='grey', label='raw, nonconfident')

            self.removeHighErrorCandidates()

            yPred = self.makePredictionVector()
            pl.scatter(self.yVector, yPred, c='yellow', label='raw, nonconfident')
            pl.xlabel('measured')
            pl.ylabel('predicted')
            pl.title('Multiple Linear Regression')
            pl.legend()
            pl.show()

            quit()

    def tryMLR(self):
        try:
            self.m = ols(array(self.yVector), array(self.xMatrix), y_varnm = 'y', x_varnm = ['x1','x2','x3','x4','x5','x6','x7','x12','x22','x32','x42','x52','x62','x72','logp', 'xblah', 'xfoo'])
            return True
        except:
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

                b = self.m.b
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
                        predScanID = b[0]
                        for propIndex in range(0, len(lookedUpPropArr)):
                            propVal = lookedUpPropArr[propIndex]
                            propCoefficient = b[propIndex + 1]
                            predScanID += propCoefficient * propVal
                    
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
            b = self.m.b
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
                predScanID = b[0]
                for propIndex in range(0, len(lookedUpPropArr)):
                    propVal = lookedUpPropArr[propIndex]
                    propCoefficient = b[propIndex + 1]
                    predScanID += propCoefficient * propVal
            
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
        #self.tryMLR()
        b = self.m.b
        summary = {}

        print("")
        print("making summary:")
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

                    metaboliteNames = nameresolver.getNames(keggID)
                    try:
                        print("resolved " + str(keggID) + " to " + metaboliteNames)
                        metaboliteSummary["names"] = metaboliteNames
                    except:
                        print("error caught while trying to resolve name")

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
    disambiguator.disambiguate()
    disambiguator.tryMLR()
    disambiguator.m.summary()
    disambiguator.printSummary()
#disambiguator.printSummary()
