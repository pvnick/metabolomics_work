#!/bin/bash

KEGGID=$1
PUBCHEMID=`mysql -uroot -s --skip-column-names -e "use metabolomics;select pubchemid from MetaboliteCandidates where keggid='$KEGGID' limit 1"`
MOLECULE_FILENAME="molecules/pubchem_"$PUBCHEMID"_3D.sdf"

VALUE=$(./utils/asacalc/asacalc $MOLECULE_FILENAME)
if [ "$VALUE" != "null" -a "$VALUE" != "" ]; then
    ./set_molecule_prop_in_db.sh "$KEGGID" "CALCULATED_ASA" "$VALUE"
fi
