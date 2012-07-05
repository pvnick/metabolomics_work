#!/bin/bash

PUBCHEM_ID=$1
SDF_2D_MOLECULE_PATH="../molecules/pubchem_"$PUBCHEM_ID"_2D.sdf"
SDF_3D_MOLECULE_PATH="../molecules/pubchem_"$PUBCHEM_ID"_3D.sdf"

curl 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?sid='$PUBCHEM_ID'&disopt=DisplaySDF' > $SDF_2D_MOLECULE_PATH 2>/dev/null
curl 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?sid='$PUBCHEM_ID'&disopt=3DDisplaySDF' > $SDF_3D_MOLECULE_PATH 2>/dev/null

#delete the 2d molecule file if there was an error
if [[ "$(cat $SDF_2D_MOLECULE_PATH)" == *"PubChem Error Report"* ]]; then
	rm -f $SDF_2D_MOLECULE_PATH
fi

#delete the 3d molecule file if there was an error
if [[ "$(cat $SDF_3D_MOLECULE_PATH)" == *"PubChem Error Report"* ]]; then
	rm -f $SDF_3D_MOLECULE_PATH
fi

