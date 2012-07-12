<?php

//this script gets all metabolites with measured scantimes from the database and joins to them all the properties we have stored about that molecule

define("MEASURED_SCANTIME_PROPERTY", "MEASURED_SCANTIME");

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
	$sql = "select
                keggid,
                value scantime
            from
                MetaboliteProperties
            where
                property='" . MEASURED_SCANTIME_PROPERTY . "'
            ";

	$result = mysql_query($sql);

	while($row = mysql_fetch_array($result))
	{
        $keggid = $row["keggid"];
        $scantime = $row["scantime"];
        $metabolites[$keggid] = array();
        $metabolites[$keggid][MEASURED_SCANTIME_PROPERTY] = (double)$scantime;
	}

	mysql_close($con);
}

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

	$result = mysql_query($sql);
    $properties = array();

	while($row = mysql_fetch_array($result))
	{
        $properties[] = $row["property"];
	}

	mysql_close($con);

    return $properties;
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
        $value = $row["value"];
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

?>
