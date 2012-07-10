#takes chemspider datasheet html in stdin and prints out all properties listed under "Predicted - ACD/Labs"
import sys
import re
import fileinput
from bs4 import BeautifulSoup

html = ""
for line in fileinput.input():
    html += line

soup = BeautifulSoup(html)
propertyTable = soup.find(id="acdlabs-table")
propertyName = ""
lookingForVal = False
for child in propertyTable.find_all("td"):
    childClass = child.get("class")[0]
    classSubstring = childClass[:10]

    if classSubstring == "prop_title":
        propertyPlaintext = child.get_text()
#convert plaintext property to some kind of identifierish thing
        property = re.sub(r'\W+', '', propertyPlaintext)
        property = "CHEMSPIDER_" + property.upper()
        sys.stdout.write(property + ",")
    elif classSubstring == "prop_value":
        valuePlaintext = child.get_text()
        valueNumericObj = re.search(r'[0-9\.\-]+', valuePlaintext)
        print(valueNumericObj.group())
    else:
        raise Exception("unexpected class name")
