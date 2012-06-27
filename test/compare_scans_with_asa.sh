#!/bin/bash

LINES=`cat known.dat`
for LINE in $LINES; do
	KEGG_ID=`echo $LINE | awk 'BEGIN{FS=","}{print $1;}'`
	SCAN=`echo $LINE | awk 'BEGIN{FS=","}{print $2;}'`
	URL="http://www.genome.jp/dbget-bin/get_linkdb?-t+pubchem+cpd:"$KEGG_ID
	PUBCHEM_ID=$(curl "$URL" 2>/dev/null | grep pubchem.ncbi.nlm.nih.gov | awk 'BEGIN{FS="\\?sid="}{print $2}' | awk 'BEGIN{FS="\">"}{print $1}')
	FILENAME="../molecules/pubchem_"$PUBCHEM_ID"_3D.sdf"
	if [ -e "$FILENAME" ]; then
		ASA=`../asacalc/asacalc "../molecules/pubchem_"$PUBCHEM_ID"_3D.sdf" 2> /dev/null`
		if [[ $ASA != "" ]]; then
			echo $ASA,$SCAN
		fi
	fi
done
