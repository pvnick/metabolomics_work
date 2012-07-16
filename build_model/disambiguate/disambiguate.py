import io
import json
import imp
import pprint
import warnings
from numpy import *

imp.load_source('ols', '../ols.py')
from ols import ols

mlrPropCombo = ["PUBCHEM_XLOGP", "3DMET_DENSITY", "3DMET_ANGLE_BEND_ENERGY"]

ambiguitiesPropsFile = open('ambiguities.json', 'r')
ambiguitiesPropsJSON = ambiguitiesPropsFile.read()
ambiguities = json.loads(ambiguitiesPropsJSON)


