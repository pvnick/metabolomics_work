#!/bin/bash

DATASHEET_FILE=$1
PLAINTEXT_PROPERTY=$2

DATASHEET_CONTENTS=`cat $DATASHEET_FILE`

echo -e "$DATASHEET_CONTENTS" | grep "  $PLAINTEXT_PROPERTY" | perl -wlne 'print $1 if / (-?[\d\.]+)/'
