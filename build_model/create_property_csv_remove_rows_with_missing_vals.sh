#!/bin/bash

mysql -uroot --skip-column-names -e"use metabolomics;
    select
        query1.val y, 
        query2.val x1, 
        query3.val x2,
        query4.val x3
    from (
        select
            keggid,
            value val 
        from
            MetaboliteProperties
        where
            property='MEASURED_SCANTIME'
            and value > 250 
    ) query1 
    join (
        select
            keggid,
            value val 
        from
            MetaboliteProperties
        where
            property='PUBCHEM_XLOGP'
    ) query2 using (keggid) 
    join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='3DMET_ANGLE_BEND_ENERGY'
    ) query3 using (keggid)
    join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='3DMET_DENSITY'
    ) query4 using (keggid)
    where
        query1.val is not null
        and query2.val is not null
        and query3.val is not null
        and query4.val is not null
" | tr '\t' ',' > properties.csv
