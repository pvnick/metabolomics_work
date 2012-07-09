#!/bin/bash

cat kegg_ids.dat | xargs -n 1 -P 20 -I {} ./lookup_and_store_keggid.sh {}
