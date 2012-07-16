<?php

echo("dont run this file unless you're absolutely sure about it! it indiscriminately adds to the ambiguities list without checking for duplicates.\nif you really want to run it, comment out the exit command below this line\n");
exit();

function createAmbiguityEntry($scanTime) {
    $con = mysql_connect('127.0.0.1', 'root');
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }

    mysql_select_db("metabolomics", $con);

    //need a list of metabolites for which we have a measured scan times
    $sql = "insert into MetaboliteAmbiguities
            (ScanID)
            VALUES
            ($scanTime)
            ";
    mysql_query($sql);
    $ambiguityID = mysql_insert_id();
    mysql_close($con);

    return $ambiguityID;
}

$originalList = file_get_contents("original_ambiguous_list.csv");
$lines = explode("\n", $originalList);
foreach ($lines as $line) {
    $csvValues = explode(",", $line);
    $metaboliteList = $csvValues[0];
    $scanTime = $csvValues[1];
    $metabolites = explode(";", $metaboliteList);
    $ambiguityID = createAmbiguityEntry($scanTime);
    foreach ($metabolites as $keggID) {
        $con = mysql_connect('127.0.0.1', 'root');
        if (!$con)
        {
            die('Could not connect: ' . mysql_error());
        }

        mysql_select_db("metabolomics", $con);

        //need a list of metabolites for which we have a measured scan times
        $sql = "insert into MetaboliteProperties
                (KeggID, Property, Value)
                VALUES
                ('$keggID', 'AMBIGUITY_ID', $ambiguityID)
                ";
        mysql_query($sql);
        mysql_close($con);

        $con = mysql_connect('127.0.0.1', 'root');
        if (!$con)
        {
            die('Could not connect: ' . mysql_error());
        }

        mysql_select_db("metabolomics", $con);

        //temporarily record the scantime in question to all ambiguous metabolites
        $sql = "insert into MetaboliteProperties
                (KeggID, Property, Value)
                VALUES
                ('$keggID', 'SUSPECTED_SCANTIME', $scanTime)
                on duplicate key update value=VALUES(value);";
        mysql_query($sql);
        mysql_close($con);
    }
}
