#!/bin/bash

KEGG_ID=$1
DATASHEET_FILE=$2
PLAINTEXT_PROPERTY_DESC=$3
PROPERTY_NAME=$4

if [ -e $DATASHEET_FILE ]; then
	PROPERTY_VALUE=`./get_molecule_property.sh $DATASHEET_FILE $PLAINTEXT_PROPERTY_DESC`
	if [ "$PROPERTY_VALUE" != "" ]; then
		../store_metabolite_properties/set_molecule_prop_in_db.sh "$KEGG_ID" "$PROPERTY_NAME" "$PROPERTY_VALUE"
	fi
fi
