September 30th 2024 by Darren Sherrell

----
This assumes that you have the latest version of EigerOnePvServer in the scripts pvservers directory. 
If not use the normal git clone command.

  
--------
NAVIGATE 

go to 
> /home/ls-cat/scripts/pvservers/EigerOnePvServer

------------------------
SET UP CONDA ENVIRONMENT

type
> conda env list

This should return a list of available conda environments. 
We want to activate the one called pvserver

> conda activate pvserver

This make a your prompt look like this:

(pvserver) ls-cat@juniper:~/scripts/pvservers/EigerOnePvServer$


-------------------
START PYTHON SERVER
> python3 EigerOnePvServer.py


------
CHECK SERVER IS WORKING

In a different terminal check these commands work (don't forget to undo them)

Try these commands and make sure the response

> GET http://localhost:5000/pv/21EIG1:cam1:NDAttributesFile
> {"pvname":"21EIG1:cam1:NDAttributesFile","value":""}


> curl -X POST -H "Content-Type: application/json" -d '{"value": "localtest"}' http://localhost:5000/pv/21EIG1:cam1:NDAttributesFile

> {"pvname":"21EIG1:cam1:NDAttributesFile","value_set_to":"localtest"}



> curl -X POST -H "Content-Type: application/json" -d '{"value": "20"}' http://localhost:5000/pv/21EIG1:cam1:NumTriggers

> {"pvname":"21EIG1:cam1:NumTriggers","value_set_to":"20"}


When there is a successful for call to the server you should see something like this from the server window

> PV Name: 21EIG1:cam1:NDAttributesFile
> PV Type: time_char
> PV Base Type: char
> PV Count: 256
> PV Value: local
> 127.0.0.1 - - [30/Sep/2024 10:40:06] "GET /pv/21EIG1:cam1:NDAttributesFile HTTP/1.1" 200 -
> PV Name: 21EIG1:cam1:NumTriggers
> PV Type: time_long
> PV Base Type: long
> PV Count: 1
> PV Value: 30
> 127.0.0.1 - - [30/Sep/2024 10:40:17] "POST /pv/21EIG1:cam1:NumTriggers HTTP/1.1" 200 -
 

-------

