#!/bin/bash

KEGG_ID=$1
PUBCHEM_URL="http://www.genome.jp/dbget-bin/get_linkdb?-t+pubchem+cpd:"$KEGG_ID
MET3D_URL="http://www.genome.jp/dbget-bin/get_linkdb?-t+3dmet+cpd:"$KEGG_ID
PUBCHEM_ID=$(curl "$PUBCHEM_URL" 2>/dev/null | grep "pubchem.ncbi.nlm.nih.gov" | awk 'BEGIN{FS="\\?sid="}{print $2}' | awk 'BEGIN{FS="\">"}{print $1}')
MET3D_ID=$(curl "$MET3D_URL" 2>/dev/null | grep "www.3dmet.dna.affrc.go.jp" | awk 'BEGIN{FS="\\?acc="}{print $2}' | awk 'BEGIN{FS="\">"}{print $1}')

#create the molecule in the database
#XXX table calls for molecule name, but we arent setting it anywhere yet
SQL="use metabolomics;
insert ignore into MetaboliteCandidates
(KeggID, PubChemID, MET3DID)
VALUES
('$KEGG_ID', $PUBCHEM_ID, '$MET3D_ID')"

mysql -uroot -e"$SQL"

#download molecule files

#XXX uncomment this to enable downloading pubchem 2d and 3d sdf files. ive already downloaded everything i need so i commented it out
#./download_molecule_files_from_pubchem.sh $PUBCHEM_ID

cd 3dmet
./download_datasheet.sh $MET3D_ID
cd ..
