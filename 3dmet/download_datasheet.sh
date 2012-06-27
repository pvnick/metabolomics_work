#!/bin/bash

MET3D_ID=$1
DATASHEET_PATH="../molecules/3dmet_"$MET3D_ID".htm"

curl 'http://www.3dmet.dna.affrc.go.jp/cgi/show_data.php?acc='$MET3D_ID > $DATASHEET_PATH 2>/dev/null

#delete the molecule if there was an erro
if [[ "$(cat $DATASHEET_PATH)" == *"Error operation"* ]]; then
	rm -f $DATASHEET_PATH
fi
