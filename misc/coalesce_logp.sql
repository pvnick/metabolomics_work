--pubchem doesnt have all the logp values, so we combine those with the calculated ones from acd, giving precedence to pubchem's
insert into MetaboliteProperties
select
    keggid, "LOGP_BEST_GUESS", finallogp
from
(
    select
        candidate.keggid, coalesce(pubchem.logp, acd.logp) finallogp
    from 
        MetaboliteCandidates candidate
        left outer join
        (
            select
                keggid,
                value logp
            from
                MetaboliteProperties
            where
                property='PUBCHEM_XLOGP'
        ) pubchem on (pubchem.keggid = candidate.keggid)
        left outer join (
            select
                keggid,
                value logp
            from
                MetaboliteProperties
            where
                property='CHEMSPIDER_ACDLOGP'
        ) acd on (acd.keggid = candidate.keggid)
) union_them
where
    finallogp is not null;
