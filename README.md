geyser_temp_analysis
====================

Library of code to extract geyser eruption times from temperature time series data.

Code can be any language that can be run on a Linux server.

Ideally, one general, parameterized algorithm can be written to evaluate all geysers that have eruption peaks.
Not all geyser eruptions have a "peak" as an eruption signature. 

Data can be found here:  http://www.geysertimes.org/datalogger/Raw%20Data/


The code should <br/>
a) read a CSV file of logged times and temperatures <br/>
b) output a CSV file of identified eruption times

=========================================================================
Here's a ranking of geyser data from "easy" to "hard" to interpret:

Peaks: <ol><li>Aurum</li> <li>Plume</li> <li>Lion</li> <li>Daisy</li> <li>Old Faithful</li> <li>Great Fountain</li> 
<li>Beehive</li> <li>Castle</li> <li>Oblong</li> <li>Turban</li></ol>
  
Plateaus (calculate durations, too): <ol><li>Artemisia</li> <li>Fountain</li> <li>Little Squirt</li> Grotto</li></ol>
  
Drops: <ol> <li>Depression</li> <li>Riverside</li></ol>