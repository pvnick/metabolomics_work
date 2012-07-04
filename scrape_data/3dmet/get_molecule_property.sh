#!/bin/bash

DATASHEET_HTML_FILE=$1
PROPERTY_NAME=$2

cat $DATASHEET_HTML_FILE | grep -A1 "$PROPERTY_NAME" | grep -A1 "lign=left>" | head -n2 | tail -n1 | sed 's/<[^>]*>//g' | sed 's/ //g'
