<?php

require("../common.php");

//this script gets all metabolites with measured scantimes from the database and joins to them all the properties we have stored about that molecule

//array indexed by keggid
$ambiguities = array();

function fillAmbiguitiesObject()
{
    global $ambiguities;

	$con = mysql_connect('127.0.0.1', 'root');
	if (!$con)
	{
		die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("metabolomics", $con);

    $sql = "select
                ambiguity_prop.keggid,
                ambiguity.ambiguityid,
                metabolite_props.property,
                metabolite_props.value
            from
                MetaboliteProperties ambiguity_prop
                join MetaboliteAmbiguities ambiguity ON (
                    ambiguity.ambiguityid = ambiguity_prop.value
                )
                join MetaboliteProperties metabolite_props ON (
                    metabolite_props.keggid = ambiguity_prop.keggid
                )
            where
                ambiguity_prop.property = 'AMBIGUITY_ID'
                and ambiguity_prop.value > 0
                and ambiguity.scanid > " . MIN_SCANTIME;

	$result = mysql_query($sql);

	while($row = mysql_fetch_array($result))
	{
        $keggid = $row["keggid"];
        $ambiguityid = (int)$row["ambiguityid"];
        $property = $row["property"];
        $value = $row["value"];

        if (!isset($ambiguities[$ambiguityid])) {
            $ambiguities[$ambiguityid] = array();
        }

        if (!isset($ambiguities[$ambiguityid][$keggid])) {
            $ambiguities[$ambiguityid][$keggid] = array();
        }

        $ambiguities[$ambiguityid][$keggid][$property] = (double)$value;
	}

	mysql_close($con);
}

fillAmbiguitiesObject();

echo json_encode($ambiguities);

?>
