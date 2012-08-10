#!/bin/bash

echo "super hydrophilic:"
cat super_hydrophilic | xargs -I{} -P20 -n1 python -c "import imp;nameresolver = imp.load_source('nameresolver', '../build_model/get_keggid_name.py');print(nameresolver.getNames('{}'))"

echo "super hydrophobic:"
cat super_hydrophobic | xargs -I{} -P20 -n1 python -c "import imp;nameresolver = imp.load_source('nameresolver', '../build_model/get_keggid_name.py');print(nameresolver.getNames('{}'))"
