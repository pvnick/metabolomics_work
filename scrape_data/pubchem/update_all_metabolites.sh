#!/bin/bash

KEGGID_PUBCHEMID_DB_ROWS=`mysql -uroot -s -e"use metabolomics; select concat(keggid,',',PubChemID) from MetaboliteCandidates where PubChemID != '';"`


for KEGGID_PUBCHEMID_ROW in $KEGGID_PUBCHEMID_DB_ROWS; do
	KEGGID=`echo $KEGGID_PUBCHEMID_ROW | awk 'BEGIN{FS=","}{print $1}'`
	PUBCHEMID=`echo $KEGGID_PUBCHEMID_ROW | awk 'BEGIN{FS=","}{print $2}'`

	./lookup_all_pubchem_properties.sh $KEGGID $PUBCHEMID
done
