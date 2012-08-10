#!/bin/bash

CID=$1

PUBCHEM_RESULT=$(lynx -dump 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?q=all&cid='$CID | grep -A1 InChIKey)
FIRST_TRY=$(echo $PUBCHEM_RESULT | head -n1 | awk 'BEGIN{FS="InChIKey: "}{print($2)}' | awk 'BEGIN{FS=" "}{print($1)}' | tr -d ' ')
echo $FIRST_TRY

exit

#i guess the rest of this crap isnt needed. stupid bash
FIRST_TRY_STRLEN=${#FIRST_TRY}
if [[ $FIRST_TRY_STRLEN -eq 27 ]]; then
    echo $FIRST_TRY
else
    echo "nope"
fi


