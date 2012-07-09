#!/bin/bash

KEGG_ID=$1
PUBCHEM_URL="http://www.genome.jp/dbget-bin/get_linkdb?-t+pubchem+cpd:"$KEGG_ID
PUBCHEM_ID=$(curl "$PUBCHEM_URL" 2>/dev/null | grep "pubchem.ncbi.nlm.nih.gov" | awk 'BEGIN{FS="\\?sid="}{print $2}' | awk 'BEGIN{FS="\">"}{print $1}')
CID=`lynx -dump 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?sid='$PUBCHEM_ID'&viewopt=PubChem' | grep 'Chemical Structure (CID' | awk 'BEGIN{FS="CID "}{print($2)}' | awk 'BEGIN{FS=")"}{print($1)}'`
INCHIKEY=$(lynx -dump 'http://pubchem.ncbi.nlm.nih.gov/toc/summary_toc.cgi?tocid=395&cid='$CID | grep 'InChIKey:' | sed 's/\[[^]]*\]//g' | awk 'BEGIN{FS="Key: "}{print($2)}')

echo $INCHIKEY
