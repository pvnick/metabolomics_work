#!/bin/bash

#get a list of all keggids and their respective ids in other databases
metabolites=`mysql -uroot --skip-column-names -s -e"use metabolomics;
select
    keggid,
    pubchemid,
    met3did
from
    MetaboliteCandidates
"`

#download needed molecule files

#cd pubchem
#resolve molecules in parallel because they're slow
#echo -e "$metabolites" | awk 'BEGIN{FS="	"}{print($2)}' | xargs -I{} -P20 -n1 ./download_molecule_files_from_pubchem.sh {}

#resolve data sheets in parallel because they're slow
#echo -e "$metabolites" | awk 'BEGIN{FS="	"}{print($2)}' | xargs -I{} -P20 -n1 ./download_pubchem_property_sheet.sh {}
#cd ..

#download 3dmet datasheet
#cd 3dmet
#./download_datasheet.sh $MET3D_ID
#cd ..

echo -e "$metabolites" | awk 'BEGIN{FS="	"}{print($1)}' | xargs -I{} -P20 -n1 ./resolve_asa_val.sh {}
