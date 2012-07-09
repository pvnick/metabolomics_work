#!/bin/bash

mysql -uroot --skip-column-names -e"use metabolomics;
    select
        query1.val y, 
        if(isnull(query2.val), 0, query2.val) x1, 
        if(isnull(query3.val), 0, query3.val) x2, 
        if(isnull(query4.val), 0, query4.val) x3, 
        if(isnull(query5.val), 0, query5.val) x4, 
        if(isnull(query6.val), 0, query6.val) x5
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
    left outer join (
        select
            keggid,
            value val 
        from
            MetaboliteProperties
        where
            property='PUBCHEM_XLOGP'
    ) query2 using (keggid) 
    left outer join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='CALCULATED_ASA'
    ) query3 using (keggid)
    left outer join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='PUBCHEM_TPSA'
    ) query4 using (keggid)
    left outer join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='3DMET_DENSITY'
    ) query5 using (keggid)
    left outer join (
        select
            keggid,
            value val
        from
            MetaboliteProperties
        where
            property='3DMET_SMR'
    ) query6 using (keggid)
" | tr '\t' ',' > properties.csv
