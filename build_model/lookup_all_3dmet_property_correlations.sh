#!/bin/bash

MET3D_PROPERTIES=`mysql -uroot -e"use metabolomics; select distinct property from MetaboliteProperties where property like '3DMET_%'"`

for MET3D_PROP in $MET3D_PROPERTIES; do
	echo $MET3D_PROP
	./get_correlation.sh $MET3D_PROP "MEASURED_SCANTIME"
done
