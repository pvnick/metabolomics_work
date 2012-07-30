import io
import json
import imp
import pprint
import warnings
from numpy import *

imp.load_source('ols', '../ols.py')
from ols import ols

MAX_RECURSION_LEVEL = 4 
COMBOS_TO_KEEP = 10

metabolitePropsFile = open('metabolite_props.json', 'r')
metabolitePropsJSON = metabolitePropsFile.read()
metabolites = json.loads(metabolitePropsJSON)

#uniqueProps = ["CHEMSPIDER_ACDBCFPH55","CHEMSPIDER_ACDBCFPH74","CHEMSPIDER_ACDKOCPH55","CHEMSPIDER_ACDKOCPH74","CHEMSPIDER_ACDLOGDPH55","CHEMSPIDER_ACDLOGDPH74","CHEMSPIDER_ACDLOGP","CHEMSPIDER_BOILINGPOINT","CHEMSPIDER_DENSITY","CHEMSPIDER_ENTHALPYOFVAPORIZATION","CHEMSPIDER_FLASHPOINT","CHEMSPIDER_FREELYROTATINGBONDS","CHEMSPIDER_HBONDACCEPTORS","CHEMSPIDER_HBONDDONORS","CHEMSPIDER_INDEXOFREFRACTION","CHEMSPIDER_MOLARREFRACTIVITY","CHEMSPIDER_MOLARVOLUME","CHEMSPIDER_OFRULEOF5VIOLATIONS","CHEMSPIDER_POLARIZABILITY","CHEMSPIDER_POLARSURFACEAREA","CHEMSPIDER_SURFACETENSION","CHEMSPIDER_VAPOURPRESSURE","PUBCHEM_COMPLEXITY","PUBCHEM_CONFORMER_SAMPLING_RMSD","PUBCHEM_COVALENTLY_BONDED_UNIT_COUNT","PUBCHEM_DEFINED_ATOM_ATEREOCENTER_COUNT","PUBCHEM_DEFINED_BOND_STEREOCENTER_COUNT","PUBCHEM_EFFECTIVE_ROTOR_COUNT","PUBCHEM_EXACT_MASS","PUBCHEM_FEATURE_3D_ACCEPTOR_COUNT","PUBCHEM_FEATURE_3D_ANION_COUNT","PUBCHEM_FORMAL_CHARGE","PUBCHEM_HBOND_ACCEPTOR","PUBCHEM_HBOND_DONOR","PUBCHEM_HEAVY_ATOM_COUNT","PUBCHEM_ISOTOPE_ATOM_COUNT","PUBCHEM_MOLECULAR_WEIGHT","PUBCHEM_MONOISOTOPIC_MASS","PUBCHEM_TPSA","PUBCHEM_UNDEFINED_ATOM_STEREOCENTER_COUNT","PUBCHEM_UNDEFINED_BOND_STEREOCENTER_COUNT","PUBCHEM_XLOGP"]
#uniqueProps = ["3DMET_ACIDIC_ATOMS","3DMET_ANGLE_BEND_ENERGY","3DMET_AROMATIC_ATOMS","3DMET_AROMATIC_BONDS","3DMET_ASA","3DMET_BASIC_ATOMS","3DMET_BOND_STRETCHBEND_ENERGY","3DMET_CHIRAL_ATOMS","3DMET_DENSITY","3DMET_DIAMETER","3DMET_DIPOLE","3DMET_DOUBLE_BONDS","3DMET_ELECTROSTATIC_ENERGY","3DMET_FORMAL_CHARGE","3DMET_GLOBULARITY","3DMET_HBOND_ACCEPTOR","3DMET_HBOND_DONOR","3DMET_HEAVY_ATOMS","3DMET_LOGP_O_TO_W","3DMET_NONBOND_ENERGY","3DMET_NUMBER_OF_ATOMS","3DMET_NUMBER_OF_BONDS","3DMET_NUMBER_OF_RINGS","3DMET_OUTOFPLANE_ENERGY","3DMET_POTENTIAL_ENERGY","3DMET_ROTATABLE_SINGLE_BONDS","3DMET_SINGLE_BONDS","3DMET_SLOGP","3DMET_SMR","3DMET_SOLVATION_ENERGY","3DMET_TORSION_ENERGY","3DMET_TPSA","3DMET_TRIPLE_BONDS","3DMET_VAN_DEL_WAALS_ENERGY","3DMET_VOLUME","3DMET_VSA","3DMET_WEIGHT","CHEMSPIDER_ACDBCFPH55","CHEMSPIDER_ACDBCFPH74","CHEMSPIDER_ACDKOCPH55","CHEMSPIDER_ACDKOCPH74","CHEMSPIDER_ACDLOGDPH55","CHEMSPIDER_ACDLOGDPH74","CHEMSPIDER_ACDLOGP","CHEMSPIDER_BOILINGPOINT","CHEMSPIDER_DENSITY","CHEMSPIDER_ENTHALPYOFVAPORIZATION","CHEMSPIDER_FLASHPOINT","CHEMSPIDER_FREELYROTATINGBONDS","CHEMSPIDER_HBONDACCEPTORS","CHEMSPIDER_HBONDDONORS","CHEMSPIDER_INDEXOFREFRACTION","CHEMSPIDER_MOLARREFRACTIVITY","CHEMSPIDER_MOLARVOLUME","CHEMSPIDER_OFRULEOF5VIOLATIONS","CHEMSPIDER_POLARIZABILITY","CHEMSPIDER_POLARSURFACEAREA","CHEMSPIDER_SURFACETENSION","CHEMSPIDER_VAPOURPRESSURE"];
uniqueProps = ["3DMET_ACIDIC_ATOMS","3DMET_ANGLE_BEND_ENERGY","3DMET_AROMATIC_ATOMS","3DMET_AROMATIC_BONDS","3DMET_ASA","3DMET_BASIC_ATOMS","3DMET_BOND_STRETCHBEND_ENERGY","3DMET_CHIRAL_ATOMS","3DMET_DENSITY","3DMET_DIAMETER","3DMET_DIPOLE","3DMET_DOUBLE_BONDS","3DMET_ELECTROSTATIC_ENERGY","3DMET_FORMAL_CHARGE","3DMET_GLOBULARITY","3DMET_HBOND_ACCEPTOR","3DMET_HBOND_DONOR","3DMET_HEAVY_ATOMS","3DMET_LOGP_O_TO_W","3DMET_NONBOND_ENERGY","3DMET_NUMBER_OF_ATOMS","3DMET_NUMBER_OF_BONDS","3DMET_NUMBER_OF_RINGS","3DMET_OUTOFPLANE_ENERGY","3DMET_POTENTIAL_ENERGY","3DMET_ROTATABLE_SINGLE_BONDS","3DMET_SINGLE_BONDS","3DMET_SLOGP","3DMET_SMR","3DMET_SOLVATION_ENERGY","3DMET_TORSION_ENERGY","3DMET_TPSA","3DMET_TRIPLE_BONDS","3DMET_VAN_DEL_WAALS_ENERGY","3DMET_VOLUME","3DMET_VSA","3DMET_WEIGHT","CHEMSPIDER_ACDBCFPH55","CHEMSPIDER_ACDBCFPH74","CHEMSPIDER_ACDKOCPH55","CHEMSPIDER_ACDKOCPH74","CHEMSPIDER_ACDLOGDPH55","CHEMSPIDER_ACDLOGDPH74","CHEMSPIDER_ACDLOGP","CHEMSPIDER_BOILINGPOINT","CHEMSPIDER_DENSITY","CHEMSPIDER_ENTHALPYOFVAPORIZATION","CHEMSPIDER_FLASHPOINT","CHEMSPIDER_FREELYROTATINGBONDS","CHEMSPIDER_HBONDACCEPTORS","CHEMSPIDER_HBONDDONORS","CHEMSPIDER_INDEXOFREFRACTION","CHEMSPIDER_MOLARREFRACTIVITY","CHEMSPIDER_MOLARVOLUME","CHEMSPIDER_OFRULEOF5VIOLATIONS","CHEMSPIDER_POLARIZABILITY","CHEMSPIDER_POLARSURFACEAREA","CHEMSPIDER_SURFACETENSION","CHEMSPIDER_VAPOURPRESSURE","PUBCHEM_COMPLEXITY","PUBCHEM_CONFORMER_SAMPLING_RMSD","PUBCHEM_COVALENTLY_BONDED_UNIT_COUNT","PUBCHEM_DEFINED_ATOM_ATEREOCENTER_COUNT","PUBCHEM_DEFINED_BOND_STEREOCENTER_COUNT","PUBCHEM_EFFECTIVE_ROTOR_COUNT","PUBCHEM_EXACT_MASS","PUBCHEM_FEATURE_3D_ACCEPTOR_COUNT","PUBCHEM_FEATURE_3D_ANION_COUNT","PUBCHEM_FORMAL_CHARGE","PUBCHEM_HBOND_ACCEPTOR","PUBCHEM_HBOND_DONOR","PUBCHEM_HEAVY_ATOM_COUNT","PUBCHEM_ISOTOPE_ATOM_COUNT","PUBCHEM_MOLECULAR_WEIGHT","PUBCHEM_MONOISOTOPIC_MASS","PUBCHEM_TPSA","PUBCHEM_UNDEFINED_ATOM_STEREOCENTER_COUNT","PUBCHEM_UNDEFINED_BOND_STEREOCENTER_COUNT","PUBCHEM_XLOGP"];

bestCombos = {} 
globalYVector = {}

def makeYVector():
    global globalYVector
    for keggID, properties in metabolites.iteritems():
        measuredScanTime = properties["MEASURED_SCANTIME"]
        globalYVector[keggID] = measuredScanTime

def recursivelyTestPropertyCombinations(currentPropComboDict, propertyStartIndex, currentRecursionLevel):
    if currentRecursionLevel >= MAX_RECURSION_LEVEL:
        propCombo = currentPropComboDict.keys()
        testMLRCombo(propCombo)
    else:
        for propIndex in range(propertyStartIndex, len(uniqueProps)):
            prop = uniqueProps[propIndex]
            if prop not in currentPropComboDict:
                currentPropComboDict[prop] = True
                recursivelyTestPropertyCombinations(currentPropComboDict, propertyStartIndex + 1, currentRecursionLevel + 1)
                del currentPropComboDict[prop]

def testMLRCombo(propCombo):
    global bestCombos
    yVector = globalYVector.copy()
    xMatrix = []
    y = []

    for keggID, scanTime in yVector.iteritems():
        xMatrixRow = [] 
        addRowToMatrix = True
        for prop in propCombo:
            if prop in metabolites[keggID]:
                value = metabolites[keggID][prop]
                xMatrixRow.append(value)
            else:
                addRowToMatrix = False
                break
        if addRowToMatrix:
            #all properties exist, add to matrix
            xMatrix.append(xMatrixRow)
            y.append(scanTime)


    try:
        m = ols(array(y), array(xMatrix), y_varnm = 'y',x_varnm = ['x1','x2','x3']) #,'x4'])
    except:
        return

    rSquared = m.R2
    if len(bestCombos) == 0:
        lowestRSquared = 0
    else:
        lowestRSquared = min(bestCombos, key = bestCombos.get)

    newBest = False
    
    if (len(bestCombos) < COMBOS_TO_KEEP):
        bestCombos[rSquared] = propCombo
        newBest = True
    elif rSquared > lowestRSquared:
        bestCombos[rSquared] = propCombo
        newBest = True
        del bestCombos[lowestRSquared]

    if newBest:
        print("")
        print("new combo:")
        print("r^2=" + str(rSquared) + ", combo=" + str(propCombo) + ", n=" + str(len(y)))
        print("summary:")
        m.summary()
        print("all saved combos:")
        pp = pprint.PrettyPrinter()
        pp.pprint(bestCombos)

#sometimes scipy generates warnings, which usually means something went wrong and we might get bad data
#to remedy this, switch all warnings to error, catch them when doing the multiple linear regression, and disregard that property combination
warnings.resetwarnings()
warnings.simplefilter('error')

makeYVector()
recursivelyTestPropertyCombinations({}, 0, 0)
pp = pprint.PrettyPrinter()
pp.pprint(bestCombos)
