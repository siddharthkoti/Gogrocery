<?php
	// extract($_GET);
    $db_connection = pg_connect("host=ec2-107-22-160-199.compute-1.amazonaws.com port=5432 dbname=d4g0u6alpfr93h user=okdddtuimwkwre password=78ae3831414769bc68dc7b281f970db0d6e24b94edc2a40462a371800c2d6b2d") or die('connection failed');;
	
	// $result = pg_query($db_connection, "SELECT * FROM product where pid = ". $pid .";" );
	$result = pg_query($db_connection, "SELECT * FROM product where pid = 'p1';" );
	
	echo $result;
	// echo "Number of rows: " . pg_numrows($result);
	
	
	
	// for ($row = 0; $row < pg_numrows($result); $row++) {        
        // $gg = pg_result($result, $row, 'id') . " ";        
        // $gg .= pg_result($result, $row, 'username') . " ";        
        // $gg .= pg_result($result, $row, 'email');        
        // echo "Customer: $gg<br>n";        
    // }  
?>

