import io
import json
import pprint

summaryFile = open('summary_list.json', 'r')
JSON = summaryFile.read()
rawSummary = eval(JSON)
finalSummary = {}
errorThreshold = 0.1

for ambiguityID, results in rawSummary.iteritems():
    finalResults = []
    for result in results:
        if result["error"] <= errorThreshold:
            if "chosen" in result:
                del result["chosen"]
            finalResults.append(result)
    if len(finalResults) > 0:
        finalSummary[ambiguityID] = finalResults
         
pp = pprint.PrettyPrinter()
pp.pprint(finalSummary)
