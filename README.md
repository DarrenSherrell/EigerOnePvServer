September 27th 2024 by Darren Sherrell

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

This should return a list of available conda environments. We want to activate the one called pvserver

> conda activate pvserver

This make a your prompt look like this:

(pvserver) ls-cat@juniper:~/scripts/pvservers/EigerOnePvServer$


-------------------
START PYTHON SERVER
(pvserver) ls-cat@juniper:~/scripts/pvservers/EigerOnePvServer$ python3 EigerOnePvServer.py


------
CHECK SERVER IS WORKING

In a different terminal check these commands work (don't forget to undo them)

Try these commands and make sure the response

> GET http://localhost:5000/pv/21EIG1:cam1:NDAttributesFile
> {"pvname":"21EIG1:cam1:NDAttributesFile","value":""}

...more on Monday
