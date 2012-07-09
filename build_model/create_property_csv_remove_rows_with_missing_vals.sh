#!/bin/bash

mysql -uroot --skip-column-names -e"use metabolomics;
    select
        query1.val y, 
        query2.val x1, 
        query3.val x2,
        query4.val x3,
        query5.val x4,
        query6.val x5
    from (
        select
            keggid,
            value val 
        from
            MetaboliteProperties
        where
            property='MEASURED_SCANTIME'
            and value > 250 
            /*and value < 2500*/ 
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
            property='CALCULATED_ASA'
    ) query3 using (keggid)
    join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='PUBCHEM_TPSA'
    ) query4 using (keggid)
    join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='3DMET_DENSITY'
    ) query5 using (keggid)
    join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='3DMET_SMR'
    ) query6 using (keggid)
    where
        query1.val is not null
        and query2.val is not null
        and query3.val is not null
        and query4.val is not null
        and query5.val is not null
        and query6.val is not null
" | tr '\t' ',' > properties.csv
