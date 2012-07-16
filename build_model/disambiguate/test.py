import json
import pprint

ambiguitiesFile = open('ambiguities.json', 'r')
ambiguitiesJSON = ambiguitiesFile.read()
ambiguities = json.loads(ambiguitiesJSON)

pp = pprint.PrettyPrinter()
pp.pprint(ambiguities)
