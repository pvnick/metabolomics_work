<?php

require "../common.php";

$originalList = file_get_contents("original_unambiguous_list.csv");
$lines = explode("\n", $originalList);
$propertyIDs = getAllUniquePropertyIDs();
$outputObject = array();

foreach ($lines as $line) {
    $csvValues = explode(",", $line);
    $keggID = $csvValues[0];
    $scanTime = $csvValues[1];

    $outputObject[$keggID] = array();

    $con = mysql_connect('127.0.0.1', 'root');
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }

    mysql_select_db("metabolomics", $con);

    foreach ($propertyIDs as $propertyID) {
        //need a list of metabolites for which we have a measured scan times
        $sql = "select
                    value
                from
                    MetaboliteProperties
                where
                    property = '" . $propertyID . "'
                    and keggid = '$keggID'
                ";

        $result = mysql_query($sql);
        if ($result) {
            $row = mysql_fetch_array($result);
            if ($row) {
                $value = (double)$row["value"];
                $outputObject[$keggID][$propertyID] = $value;
            }
        }

    }
    mysql_close($con);
}

echo(json_encode($outputObject));
?>
