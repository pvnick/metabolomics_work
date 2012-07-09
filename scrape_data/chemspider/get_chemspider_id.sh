#!/bin/bash

#takes in inchikey as parameter, returns chemspider id
INCHIKEY=$1
CHEMSPIDERID=$(curl -I 'http://www.chemspider.com/Search.aspx?q='$INCHIKEY 2> /dev/null| grep -i location | awk 'BEGIN{FS="Structure\."}{print($2)}' | awk 'BEGIN{FS="\.html"}{print($1)}')
echo $CHEMSPIDERID
