#!/bin/bash

NUMERIC_PUBCHEM_PROPERTIES=`mysql -uroot -s --skip-column-names -e "use metabolomics; select distinct property from MetaboliteProperties where property like 'pubchem%'"`

for PUBCHEM_PROP in $NUMERIC_PUBCHEM_PROPERTIES; do
	echo $PUBCHEM_PROP
	./get_correlation.sh $PUBCHEM_PROP "SUSPECTED_SCANTIME"
done
