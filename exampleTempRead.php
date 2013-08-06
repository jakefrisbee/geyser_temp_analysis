<?php
/************************************
*  Example of peak detection method
*   using small Aurum dataset
*
*/
	ini_set('memory_limit', '-1');
	
	// read CSV file
	$theArray = readcsv('http://www.geysertimes.org/datalogger/Raw%20Data/Aurum/Aurum_Geyser%2011-21-11%20to%203-24-12.csv');
	// execute method
	$results = simple_peak_method($theArray);
	// see results
	print_r($results);
	//echo as CSV
	echo arrayToCSV($results);
	

/************************************
*  Simple Peak Detection Method
*
*/
function simple_peak_method($tempArray) {
	
	$tempBump = 10;
	$tempThreshold = 80;
	$jumpAhead = 120;
	//cumulative moving average length
	$cmaLag = 60;
	
	$arrCount = count($tempArray);
	
	$i = 1;
	do {
		if ( // determining eruption logic happens here
			(($tempArray[$i + 1][3] - $tempArray[$i][3]) >= $tempBump)
			||
			$tempArray[$i + 1][3] >= $tempThreshold
		   )
		{ // then add to final array
			$eruptionArray[] = $tempArray[$i + 1][1] . ' ' . $tempArray[$i + 1][2];
			$i = $i + $jumpAhead;
		}
		$i++;
	} while ($i < $arrCount - 1);
	
	return $eruptionArray;
}

/************************************
*  readCSV() 
*	loads CSV file into an array
*/
function readCSV($csvFile){
	$file_handle = fopen($csvFile, 'r');
	while (!feof($file_handle) ) {
		$line_of_text[] = fgetcsv($file_handle, 1024);
	}
	fclose($file_handle);
	return $line_of_text;
}
/************************************
*  cumm_moving_average()
* 	utility function for calculating a moving average
*/
function cumm_moving_average($array,$from,$to) {
	$arrCount = count($array);
	$start = max($from,0);
	$end = min($arrCount - 1,$to);
	$cma = 0;
	
	for ($j = $start; $j < $end; $j++) {
			$cma = $cma + $array[$j]['Temp'];
		}
	return $cma / ($from - $to);
}
/**
  * Formats a line (passed as a fields  array) as CSV and returns the CSV as a string.
  * Adapted from http://us3.php.net/manual/en/function.fputcsv.php#87120
  */
function arrayToCsv( array &$fields, $delimiter = ';', $enclosure = '"', $encloseAll = false, $nullToMysqlNull = false ) {
    $delimiter_esc = preg_quote($delimiter, '/');
    $enclosure_esc = preg_quote($enclosure, '/');

    $output = array();
    foreach ( $fields as $field ) {
        if ($field === null && $nullToMysqlNull) {
            $output[] = 'NULL';
            continue;
        }

        // Enclose fields containing $delimiter, $enclosure or whitespace
        if ( $encloseAll || preg_match( "/(?:${delimiter_esc}|${enclosure_esc}|\s)/", $field ) ) {
            $output[] = $enclosure . str_replace($enclosure, $enclosure . $enclosure, $field) . $enclosure;
        }
        else {
            $output[] = $field;
        }
    }

    return implode( $delimiter, $output );
}
?>