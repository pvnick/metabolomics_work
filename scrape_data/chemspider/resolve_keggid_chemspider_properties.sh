#!/bin/bash

KEGG_ID=$1

INCHIKEY=`mysql -uroot -s --skip-column-names -e"use metabolomics;select inchikey from MetaboliteCandidates where keggid='$KEGG_ID'"`
CHEMSPIDER_ID=`./get_chemspider_id.sh "$INCHIKEY"`
CHEMSPIDER_URL="http://www.chemspider.com/Chemical-Structure."$CHEMSPIDER_ID".html"
CHEMSPIDER_PAGE_CONTENTS=`curl "$CHEMSPIDER_URL" 2>/dev/null`
CHEMSPIDER_PROPERTIES=`echo -e "$CHEMSPIDER_PAGE_CONTENTS" | python get_chemspider_properties.py`
for PROP_VAL in $CHEMSPIDER_PROPERTIES; do
    PROP=`echo $PROP_VAL | awk 'BEGIN{FS=","}{print($1)}'`
    VAL=`echo $PROP_VAL | awk 'BEGIN{FS=","}{print($2)}'`
    ../set_molecule_prop_in_db.sh "$KEGG_ID" "$PROP" "$VAL"
done
