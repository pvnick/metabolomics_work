#!/bin/bash

KEGG_ID=$1
PUBCHEM_ID=$2

SDF_2D_MOLECULE_PATH="../molecules/pubchem_"$PUBCHEM_ID"_2D.sdf"
SDF_3D_MOLECULE_PATH="../molecules/pubchem_"$PUBCHEM_ID"_3D.sdf"

NUMERIC_PUBCHEM_PROPERTIES="PUBCHEM_MOLECULAR_WEIGHT	PUBCHEM_MONOISOTOPIC_WEIGHT	PUBCHEM_EXACT_MASS	PUBCHEM_TOTAL_CHARGE	PUBCHEM_COMPONENT_COUNT	PUBCHEM_HEAVY_ATOM_COUNT	PUBCHEM_ISOTOPIC_ATOM_COUNT	PUBCHEM_ATOM_DEF_STEREO_COUNT	PUBCHEM_ATOM_UDEF_STEREO_COUNT	PUBCHEM_BOND_DEF_STEREO_COUNT	PUBCHEM_BOND_UDEF_STEREO_COUNT	PUBCHEM_CACTVS_TAUTO_COUNT	PUBCHEM_CACTVS_HBOND_ACCEPTOR	PUBCHEM_CACTVS_HBOND_DONOR	PUBCHEM_CACTVS_ROTATABLE_BOND	PUBCHEM_CACTVS_COMPLEXITY	PUBCHEM_CACTVS_TPSA	PUBCHEM_XLOGP3	PUBCHEM_XLOGP3_AA	PUBCHEM_OPENEYE_TAUTO_COUNT	PUBCHEM_EFFECTIVE_ROTOR_COUNT	PUBCHEM_CONFORMER_RMSD	PUBCHEM_SHAPE_VOLUME	PUBCHEM_MMFF94_ENERGY	PUBCHEM_SHAPE_SELFOVERLAP	PUBCHEM_FEATURE_SELFOVERLAP"			

for PUBCHEM_PROP in $NUMERIC_PUBCHEM_PROPERTIES; do
	./lookup_and_set_molecule_prop_if_present.sh $SDF_2D_MOLECULE_PATH $KEGG_ID $PUBCHEM_PROP
	./lookup_and_set_molecule_prop_if_present.sh $SDF_3D_MOLECULE_PATH $KEGG_ID $PUBCHEM_PROP
done
