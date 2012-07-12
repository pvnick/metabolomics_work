#!/bin/bash

NUMERIC_CHEMSPIDER_PROPERTIES=`mysql -uroot -s --skip-column-names -e "use metabolomics; select distinct property from MetaboliteProperties where property like 'chemspider%'"`

for CHEMSPIDER_PROP in $NUMERIC_CHEMSPIDER_PROPERTIES; do
	echo $CHEMSPIDER_PROP
	./get_correlation.sh $CHEMSPIDER_PROP "MEASURED_SCANTIME"
done
