#!/bin/bash

#looks in a molecule file of a specified keggid for a property and, if found, updates that molecule's property in the db
MOLECULE_FILE=$1
KEGG_ID=$2
PROPERTY=$3

VALUE=$(../get_molecule_property/get_molecule_property $MOLECULE_FILE $PROPERTY 2> /dev/null)
if [ "$VALUE" != "null" -a "$VALUE" != "" ]; then
#found valid property
	./set_molecule_prop_in_db.sh $KEGG_ID $PROPERTY $VALUE
fi
	
