#!/bin/bash

LINES=`cat known.dat`
for LINE in $LINES; do
	KEGG_ID=`echo $LINE | awk 'BEGIN{FS=","}{print $1;}'`
	SCAN=`echo $LINE | awk 'BEGIN{FS=","}{print $2;}'`
	mysql -uroot -e "use metabolomics;
		insert into MetaboliteProperties
		(KeggID, Property, Value)
		VALUES
		('$KEGG_ID', 'MEASURED_SCANTIME', $SCAN)
		ON DUPLICATE KEY UPDATE Value=VALUES(Value);"

done
