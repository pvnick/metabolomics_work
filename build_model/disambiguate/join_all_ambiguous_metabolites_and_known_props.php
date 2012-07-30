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
                ambiguity_candidate.keggid,
                ambiguity.ambiguityid,
                ambiguity.scanid,
                metabolite_props.property,
                metabolite_props.value
            from
                MetaboliteAmbiguityCandidates ambiguity_candidate
                join MetaboliteAmbiguities ambiguity ON (
                    ambiguity.ambiguityid = ambiguity_candidate.ambiguityid
                )
                join MetaboliteProperties metabolite_props ON (
                    metabolite_props.keggid = ambiguity_candidate.keggid
                )
            where
                ambiguity.scanid > " . MIN_SCANTIME;

	$result = mysql_query($sql);

	while($row = mysql_fetch_array($result))
	{
        $keggid = $row["keggid"];
        $scanid = $row["scanid"];
        $ambiguityid = (int)$row["ambiguityid"];
        $property = $row["property"];
        $value = $row["value"];

        if (!isset($ambiguities[$ambiguityid])) {
            $ambiguities[$ambiguityid] = array(
                "scanid" => $scanid,
                "candidates" => array()
            );
        }

        
        if (!isset($ambiguities[$ambiguityid][$keggid])) {
            $ambiguities[$ambiguityid]["candidates"][$keggid] = array();
        }

        $ambiguities[$ambiguityid]["candidates"][$keggid][$property] = (double)$value;
	}

	mysql_close($con);
}

fillAmbiguitiesObject();

echo json_encode($ambiguities);

?>
