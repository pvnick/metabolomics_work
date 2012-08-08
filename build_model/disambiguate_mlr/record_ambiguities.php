<?php

echo("dont run this file unless you're absolutely sure about it! it indiscriminately adds to the ambiguities list without checking for duplicates.\nif you really want to run it, comment out the exit command below this line\n");
exit();

function createAmbiguityEntry($scanTime, $confident) {
    $confident = (string)$confident;
    $con = mysql_connect('127.0.0.1', 'root');
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }

    mysql_select_db("metabolomics", $con);

    //need a list of metabolites for which we have a measured scan times
    $sql = "insert into MetaboliteAmbiguities
            (ScanID, Confident)
            VALUES
            ($scanTime, $confident)
            ";
    mysql_query($sql);
    $ambiguityID = mysql_insert_id();
    mysql_close($con);

    return $ambiguityID;
}

function makeMetaboliteInstanceAmbiguitiesUnconfident($keggID) {
    //by default, keggids listed by themselves will get recorded as "confident" which means they only appear once and by themselves - we're confident they appeared when listed
    //when that same keggid appears again, either with another scan id or as part of a list, we change the confident setting to false
    $con = mysql_connect('127.0.0.1', 'root');
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }

    mysql_select_db("metabolomics", $con);

    $sql = "update 
                MetaboliteAmbiguities
            set 
                Confident = 0
            where
                ambiguityid in (
                    select
                        ambiguityid
                    from 
                        MetaboliteAmbiguityCandidates
                    where
                        keggid = '$keggID'
                ) 
            ";

    mysql_query($sql);
    mysql_close($con);
}

function noLongerConfident($keggID) {
    $con = mysql_connect('127.0.0.1', 'root');
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }

    mysql_select_db("metabolomics", $con);

    $sql = "select
                count(1) cnt
            from 
                MetaboliteAmbiguityCandidates
            where
                keggid = '$keggID'";

	$result = mysql_query($sql);
    $row = mysql_fetch_array($result);
    return ($row["cnt"] > 1);
}


function insertAmbiguityCandidate($ambiguityID, $keggID) {
    $con = mysql_connect('127.0.0.1', 'root');
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }

    mysql_select_db("metabolomics", $con);

    //add each possible metabolite as a candidate for this ambiguity
    $sql = "insert into MetaboliteAmbiguityCandidates
            (AmbiguityID, KeggID)
            VALUES
            ($ambiguityID, '$keggID')
            ";
    mysql_query($sql);
    mysql_close($con);
}


$originalList = file_get_contents("scantimes.csv");
$lines = explode("\n", $originalList);
foreach ($lines as $line) {
    $confident = "1";
    $csvValues = explode(",", $line);
    $metaboliteList = $csvValues[0];
    $scanTime = $csvValues[1];
    $metabolites = explode(";", $metaboliteList);
    if (count($metabolites) > 1) {
        $confident = "0";
    }
    $ambiguityID = createAmbiguityEntry($scanTime, $confident);
    foreach ($metabolites as $keggID) {
        insertAmbiguityCandidate($ambiguityID, $keggID);
        
        if (noLongerConfident($keggID)) {
            makeMetaboliteInstanceAmbiguitiesUnconfident($keggID);
        }

    }
}
