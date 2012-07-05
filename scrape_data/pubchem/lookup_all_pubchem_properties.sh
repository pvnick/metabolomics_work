#!/bin/bash

KEGG_ID=$1
PUBCHEM_ID=$2

DATASHEET_FILE="../molecules/pubchem_"$PUBCHEM_ID"_data.dat"

./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Molecular Weight" "PUBCHEM_MOLECULAR_WEIGHT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "XLogP3-AA" "PUBCHEM_XLOGP"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "H-Bond Donor" "PUBCHEM_HBOND_DONOR"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "H-Bond Acceptor" "PUBCHEM_HBOND_ACCEPTOR"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Rotatable Bond Count" "ROTATABLE_BOND_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Exact Mass" "PUBCHEM_EXACT_MASS"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "MonoIsotopic Mass" "PUBCHEM_MONOISOTOPIC_MASS"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Topological Polar Surface Area" "PUBCHEM_TPSA"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Heavy Atom Count" "PUBCHEM_HEAVY_ATOM_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Formal Charge" "PUBCHEM_FORMAL_CHARGE"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Complexity" "PUBCHEM_COMPLEXITY"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Isotope Atom Count" "PUBCHEM_ISOTOPE_ATOM_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Defined Atom Stereocenter Count" "PUBCHEM_DEFINED_ATOM_ATEREOCENTER_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Undefined Atom Stereocenter Count" "PUBCHEM_UNDEFINED_ATOM_STEREOCENTER_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Defined Bond Stereocenter Count" "PUBCHEM_DEFINED_BOND_STEREOCENTER_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Undefined Bond Stereocenter Count" "PUBCHEM_UNDEFINED_BOND_STEREOCENTER_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Covalently-Bonded Unit Count" "PUBCHEM_COVALENTLY_BONDED_UNIT_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Feature 3D Acceptor Count" "PUBCHEM_FEATURE_3D_ACCEPTOR_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Feature 3D Anion Count" "PUBCHEM_FEATURE_3D_ANION_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Effective Rotor Count" "PUBCHEM_EFFECTIVE_ROTOR_COUNT"
./store_molecule_property_if_extant.sh $KEGG_ID $DATASHEET_FILE "Conformer Sampling RMSD" "PUBCHEM_CONFORMER_SAMPLING_RMSD"
