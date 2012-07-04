#!/bin/bash

KEGGID_PUBCHEMID_DB_ROWS=`mysql -uroot -s -e"use metabolomics; select concat(keggid,',',pubchemid) from MetaboliteCandidates;"`


for KEGGID_PUBCHEMID_ROW in $KEGGID_PUBCHEMID_DB_ROWS; do
	KEGGID=`echo $KEGGID_PUBCHEMID_ROW | awk 'BEGIN{FS=","}{print $1}'`
	PUBCHEMID=`echo $KEGGID_PUBCHEMID_ROW | awk 'BEGIN{FS=","}{print $2}'`

	ASA=`../asacalc/asacalc "../molecules/pubchem_"$PUBCHEMID"_3D.sdf" 2> /dev/null`
	if [ "$ASA" != "null" -a "$ASA" != "" ]; then
		./set_molecule_prop_in_db.sh $KEGGID "SOLVENT_ACCESSIBLE_SURFACE_AREA" "$ASA"
	fi

	./lookup_all_pubchem_properties.sh $KEGGID $PUBCHEMID
done
