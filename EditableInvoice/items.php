<?php
session_start();
$dbcon=mysqli_connect("localhost","root","");
mysqli_select_db($dbcon,"sales");

	$sql = "select item from item";
	$res=mysqli_query($dbcon,$sql);
	$result="";
    while($row=mysqli_fetch_array($res)){
		$result=$result."<option value='{$row['item']}'></option>";
	}
 echo $result;
?>