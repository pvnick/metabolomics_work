#!/bin/bash

KEGGID_3DMETID_DB_ROWS=`mysql -uroot -s -e"use metabolomics; select concat(keggid,',',met3did) from MetaboliteCandidates where met3did != '';"`


for KEGGID_3DMETID_ROW in $KEGGID_3DMETID_DB_ROWS; do
	KEGGID=`echo $KEGGID_3DMETID_ROW | awk 'BEGIN{FS=","}{print $1}'`
	MET3DID=`echo $KEGGID_3DMETID_ROW | awk 'BEGIN{FS=","}{print $2}'`

	./lookup_all_3dmet_properties.sh $KEGGID $MET3DID
done
