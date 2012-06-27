#!/bin/bash

#this script expects you to do your own sql field sanitization!
KEGG_ID=$1
PROPERTY=$2
VALUE=$3

mysql -uroot -e "use metabolomics;
	insert into MetaboliteProperties
	(KeggID, Property, Value)
	VALUES
	('$KEGG_ID', '$PROPERTY', $VALUE )
	on duplicate key update value=VALUES(value);"
