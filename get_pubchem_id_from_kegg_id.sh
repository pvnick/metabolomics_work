#!/bin/bash

KEGG_ID=$1
URL="http://www.genome.jp/dbget-bin/get_linkdb?-t+pubchem+cpd:"$KEGG_ID
PUBCHEM_ID=$(curl "$URL" 2>/dev/null | grep pubchem.ncbi.nlm.nih.gov | awk 'BEGIN{FS="\\?sid="}{print $2}' | awk 'BEGIN{FS="\">"}{print $1}')
echo $KEGG_ID:$PUBCHEM_ID
