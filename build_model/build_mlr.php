<?php

require "regression_library/Matrix.php";
require "regression_library/Regression.php";


function getData() {
	$con = mysql_connect('127.0.0.1', 'root');
	if (!$con)
	{
		die('Could not connect: ' . mysql_error());
	}

	mysql_select_db("metabolomics", $con);

	$sql = "select
				query1.val y, query2.val x1, query3.val x2 
			from (
				select
					keggid,
					value val 
				from
					MetaboliteProperties
				where
					property='MEASURED_SCANTIME'
			) query1 
			join (
				select
					keggid,
					value+1 val	
				from
					MetaboliteProperties
				where
					property='3DMET_LOGP_O_TO_W'
			) query2 using (keggid) 
			join (
				select
					keggid,
					value val
				from
					MetaboliteProperties
				where
					property='3DMET_LOGP_O_TO_W'
			) query3 using (keggid)
			where
				query1.val is not null
				and query2.val is not null
				and query3.val is not null";

	$result = mysql_query($sql);
	$y = array();
	$xMatrix = array();

	while($row = mysql_fetch_array($result))
	{
		$y[] = array((float)$row["y"]);
		$xMatrix[] = array(1, (float)$row["x1"], (float)$row["x2"]);
	}


	$reg = new Lib_Regression();
	$reg->setX($xMatrix);
	$reg->setY($y);
    echo(json_encode($xMatrix) . "\n");
    echo(json_encode($y));

	//NOTE: passing true to the compute method generates standardized coefficients
	$reg->Compute();    //go!

	//var_dump($reg->getSSE());
	//var_dump($reg->getSSR());
	//var_dump($reg->getSSTO());
	echo "R^2\n";
	var_dump($reg->getRSQUARE());
	//var_dump($reg->getF());
	echo "r^2 p value\n";
	var_dump($reg->getRSQUAREPValue());
	//var_dump($reg->getCoefficients());
	//var_dump($reg->getStandardError());
	//var_dump($reg->getTStats());
	//var_dump($reg->getPValues());

	mysql_close($con);
}

getData();
?>
