<?php

//this is a really dumb, brute-force approach that tests every property combination and selects the ones with the best r^2
//could be really improved with a better algorithm. genetic algorithm comes to mind...

require_once("common.php");
require "../regression_library/Matrix.php";
require "../regression_library/Regression.php";



define("MAX_RECURSION_LEVEL", 4);
define("COMBOS_TO_KEEP", 10);

$metabolites = json_decode(file_get_contents("metabolite_props.json"), true);
$propertyIDs = getAllUniquePropertyIDs();
$bestCombos = array(); //constantly sorted downward by correlation
$globalYVector = array();

function makeYVector()
{
    global $globalYVector;
    global $metabolites;
    foreach ($metabolites as $keggID => $properties) {
        $measuredScanTime = $properties[MEASURED_SCANTIME_PROPERTY];
        $globalYVector[$keggID] = array($measuredScanTime);
    }
}

function testMLRCombo($propCombo)
{
    global $metabolites;
    global $globalYVector;
    global $bestCombos;

    $yVector = array();
    foreach ($globalYVector as $keggID => $measuredScanTime) {
        $yVector[$keggID] = $measuredScanTime;
    }
	$xMatrix = array();

    
    foreach ($yVector as $keggID => $scanTime) {
        $xMatrixRow = array(1);
        foreach ($propCombo as $propertyID) {
            if (isset($metabolites[$keggID][$propertyID])) {
                $value = $metabolites[$keggID][$propertyID];
                $xMatrixRow[] = $value;
            } else {
                //no property value for this metabolite, ignore it in the regression analysis
                unset($yVector[$keggID]);
                //skip the rest of the properties for this molecule
                continue 2;
            }
        }
        //all properties extant, add to the matrix
        $xMatrix[] = $xMatrixRow;
    }

    $y = array_values($yVector);

	$reg = new Lib_Regression();
	$reg->setX($xMatrix);
	$reg->setY($y);
    try {
        $reg->Compute(); 
        $rSquared = $reg->getRSQUARE();

        $topRSquareds = array_keys($bestCombos);
        $lowestRSquared = end($topRSquareds);
        //have to check that 0 < rSquared < 1 because sometimes the regression library flips out and returns negative
        if (($rSquared > 0 && $rSquared < 1) && (count($bestCombos) < COMBOS_TO_KEEP || $rSquared > $lowestRSquared)) {
            //found a combo with a high r-squared. add it to the list, re-sort, and snip off the one with the lowest r-squared
            $bestCombos[(string)$rSquared] = $propCombo;
            krsort($bestCombos); 
            array_splice($bestCombos, COMBOS_TO_KEEP);
            echo("new combo:\n");
            echo("r^2=" . $rSquared . ", combo=" . json_encode($propCombo) . ", n=" . count($yVector) . "\n");
            echo("all saved combos:\n");
            var_dump($bestCombos);
            echo("\n");


        }   
    } catch(Exception $e) {}
}

function recursivelyTestPropertyCombinations($currentPropComboAssocArr, $currentRecursionLevel)
{
    //$currentPropComboAssocArr is associative for fast key-based lookup of the property
    global $propertyIDs;

    if ($currentRecursionLevel >= MAX_RECURSION_LEVEL) {
        $propCombo = array_keys($currentPropComboAssocArr);
        testMLRCombo($propCombo);
    } else {
        foreach ($propertyIDs as $property) {
            if (!isset($currentPropComboAssocArr[$property])) {
                $currentPropComboAssocArr[$property] = true;
                recursivelyTestPropertyCombinations($currentPropComboAssocArr, $currentRecursionLevel + 1);
                unset($currentPropComboAssocArr[$property]);
            }
        }
    }
}

makeYVector();
recursivelyTestPropertyCombinations(array(), 0);

echo("all done!\nbest combos:\n");
var_dump($bestCombos);

?>
