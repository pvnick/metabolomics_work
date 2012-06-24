#!/bin/bash

cat kegg_ids.dat | xargs -n 1 -P 10 -I {} ./get_pubchem_id_from_kegg_id.sh {}
