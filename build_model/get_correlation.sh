#!/bin/bash

PROP1=$1
PROP2=$2

mysql -uroot -e"use metabolomics
create temporary table sample( x float not null, y float not null );
insert into sample 
select
x, y
from (
    select
        keggid,
        value x
    from
        MetaboliteProperties
    where
        property='$PROP1'
        and value > 250
) query1 join (
    select
        keggid,
        value y
    from
        MetaboliteProperties
    where
        property='$PROP2'
) query2 using (keggid);

select @ax := avg(x), 
       @ay := avg(y), 
       @div := (stddev_samp(x) * stddev_samp(y))
from sample;

select 
    sum( ( x - @ax ) * (y - @ay) ) / ((count(x) -1) * @div) Correlation
from sample;

select
	count(1) SamleSize
from sample;

"

