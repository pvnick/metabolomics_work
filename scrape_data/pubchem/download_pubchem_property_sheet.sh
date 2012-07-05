#!/bin/bash

PUBCHEM_ID=$1
PROPERTY_SHEET_PATH="../molecules/pubchem_"$PUBCHEM_ID"_data.dat"

CID=`lynx -dump 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?sid='$PUBCHEM_ID'&viewopt=PubChem' | grep 'Chemical Structure (CID' | awk 'BEGIN{FS="CID "}{print($2)}' | awk 'BEGIN{FS=")"}{print($1)}'`

#lynx dump is magic!
echo "looking up data sheet for pubchem substance $PUBCHEMID (CID $CID)"
lynx -dump 'http://pubchem.ncbi.nlm.nih.gov/toc/summary_toc.cgi?tocid=27&cid='$CID > $PROPERTY_SHEET_PATH
