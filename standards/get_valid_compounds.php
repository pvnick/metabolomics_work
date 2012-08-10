<?php

//this script looks up all the compounds we have in the lab and checks to see that they work for the model, ie they exist in the database and we have all the needed properties
//then it predicts elution times based on the following coefficients

$coefficients = array("-2306.763299","-160.016604","-16.107915","3.496028","15.245099","-18.877700","17.582158","-3.831472","-1.651341","22.148340","-301.641304","-56.345705","10.011604","-39.893671","0.716607","5.021079","82.064674","-36.373044");

function lookupCompound($inchiKey)
{
    $props = array();
	$con = mysql_connect('127.0.0.1', 'root');
	if (!$con)
	{
		die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("metabolomics", $con);

	$sql = "select
                props.property,
                props.value
            from
                MetaboliteCandidates candidate
                join MetaboliteProperties props using(keggid)
            where
                candidate.inchikey='" . $inchiKey . "'";

	$result = mysql_query($sql);

	while($row = mysql_fetch_array($result))
	{
        $prop = $row["property"];
        $value = $row["value"];
        $props[$prop] = $value;
	}

	mysql_close($con);

    return $props;
}

function predictScanID($propVals, $mlrProps) 
{
    global $coefficients;
    $predScanID = $coefficients[0];
    $bID = 1;
    foreach ($mlrProps as $prop) {
        $val = $propVals[$prop];
        $predDelta = $coefficients[$bID] * $val;
        $predScanID += $predDelta;
        $bID++;
    }
    return $predScanID;
}

$mlrProps = array('PUBCHEM_EFFECTIVE_ROTOR_COUNT', 'CHEMSPIDER_ACDBCFPH55', 'CHEMSPIDER_ACDKOCPH55', 'CHEMSPIDER_MOLARVOLUME', 'PUBCHEM_MONOISOTOPIC_MASS', 'CHEMSPIDER_ACDBCFPH74', 'CHEMSPIDER_ACDKOCPH74', 'CHEMSPIDER_FLASHPOINT', 'CHEMSPIDER_ENTHALPYOFVAPORIZATION', 'PUBCHEM_UNDEFINED_ATOM_STEREOCENTER_COUNT', 'CHEMSPIDER_OFRULEOF5VIOLATIONS', 'CALCULATED_ASA', 'CHEMSPIDER_ACDLOGDPH55', 'CHEMSPIDER_ACDLOGDPH74', 'LOGP_BEST_GUESS', 'PUBCHEM_HBOND_ACCEPTOR', 'PUBCHEM_HBOND_DONOR');

$compoundListContents = file_get_contents("lab_chemical_catalogue");
$compounds = explode("\n", $compoundListContents);
foreach($compounds as $compoundEntry) {
    $items = explode("\t", $compoundEntry);
    if (count($items) == 2) {
        $name = $items[0];
        $pubchemCID = $items[1];
        $inchikey = trim(system("./get_inchikey_from_cid.sh $pubchemCID"));
        if (strlen($inchikey) == 27) {
            $propVals = lookupCompound($inchikey); 
            $isValid = true;
            foreach ($mlrProps as $requiredProp) {
                if (!isset($propVals[$requiredProp])) {
                    $isValid = false;
                }
            }
            if ($isValid) {
                $predictedScanID = predictScanID($propVals, $mlrProps);
                echo("VALID: " . $name . ", predicted scanid=$predictedScanID\n");
            }
        }
    }
}


?>
