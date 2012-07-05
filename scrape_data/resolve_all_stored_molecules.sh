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

cd pubchem
#uncomment this to enable downloading pubchem 2d and 3d sdf files. ive already downloaded everything i need so i commented it out
#./download_molecule_files_from_pubchem.sh $PUBCHEM_ID

#resolve data sheets in parallel because they're slow
echo -e "$metabolites" | awk 'BEGIN{FS="	"}{print($2)}' | xargs -I{} -P20 -n1 ./download_pubchem_property_sheet.sh {}
cd ..

#uncomment this to enable downloading 3dmet datasheet
#cd 3dmet
#./download_datasheet.sh $MET3D_ID
#cd ..
