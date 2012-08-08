import urllib2
from bs4 import BeautifulSoup

def getNames(keggID):
    url = "http://www.genome.jp/dbget-bin/www_bget?cpd:" + keggID
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    nameLabel = soup.find("nobr", text="Name")
    nameContainer = nameLabel.parent.nextSibling.nextSibling
    unprocessedNames = nameContainer.contents[0].text
    return unprocessedNames.replace("\n","")
