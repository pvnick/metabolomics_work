<?php

define("MIN_SCANTIME", 250); //metabolites with scan times below this threshold dont work well with MLR
define("MEASURED_SCANTIME_PROPERTY", "MEASURED_SCANTIME");

function getAllUniquePropertyIDs()
{
	$con = mysql_connect('127.0.0.1', 'root');
	if (!$con)
	{
		die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("metabolomics", $con);

    //need a list of metabolites for which we have a measured scan times
	$sql = "select
                distinct property
            from
                MetaboliteProperties
            ";
            /*
            where
                property like 'PUBCHEM%'
                or property like 'CHEMSPIDER%'
                or property like '3DMET%'
            ";
            */

	$result = mysql_query($sql);
    $properties = array();

	while($row = mysql_fetch_array($result))
	{
        $properties[] = $row["property"];
	}

	mysql_close($con);

    return $properties;
}

?>
