<?php

require_once("../common.php");

//this script gets all metabolites with measured scantimes from the database and joins to them all the properties we have stored about that molecule

//array indexed by keggid
$metabolites = array();

function initializeMetaboliteArray() 
{
    global $metabolites;

	$con = mysql_connect('127.0.0.1', 'root');
	if (!$con)
	{
		die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("metabolomics", $con);

    //need a list of metabolites for which we have a measured scan times
    //also, only select metabolites with scan times greater than MIN_SCANTIME because mlr doesnt work well with the ones below that
	$sql = "select
                cand.keggid,
                amb.scanid
            from 
                MetaboliteAmbiguities amb
                join MetaboliteAmbiguityCandidates cand using (ambiguityid)
            where
                amb.confident = 1
                and amb.scanid > " . MIN_SCANTIME;

	$result = mysql_query($sql);

	while($row = mysql_fetch_array($result))
	{
        $keggid = $row["keggid"];
        $scantime = (double)$row["scanid"];
        $metabolites[$keggid] = array();
        $metabolites[$keggid][MEASURED_SCANTIME_PROPERTY] = (double)$scantime;
	}

	mysql_close($con);
}

function addPropValuesToMetabolitesArray($propertyID)
{
    global $metabolites;
    $keggIDs = array_keys($metabolites);
    $sqlArrayExpression = "'" . implode("','", $keggIDs) . "'";

	$con = mysql_connect('127.0.0.1', 'root');
	if (!$con)
	{
		die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("metabolomics", $con);

    //need a list of metabolites for which we have a measured scan times
	$sql = "select
                keggid,
                value
            from
                MetaboliteProperties
            where
                property = '" . $propertyID . "'
                and keggid in (" . $sqlArrayExpression . ")
            ";

	$result = mysql_query($sql);

	while($row = mysql_fetch_array($result))
	{
        $keggID = $row["keggid"];
        $value = (double)$row["value"];
        $metabolites[$keggID][$propertyID] = $value;
	}

	mysql_close($con);

    return $metabolites;
}

initializeMetaboliteArray();
$propertyIDs = getAllUniquePropertyIDs();
foreach ($propertyIDs as $propertyID) {
    addPropValuesToMetabolitesArray($propertyID);
}

echo json_encode($metabolites);

?>
