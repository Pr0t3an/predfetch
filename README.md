# predfetch
Python3 Prefetch Parser built using pyscca python bindings for libscca which enables it to be platform independent. Untested outside of MAC

Acknowledgements: libscca

Copyright (C) 2011-2022, Joachim Metz <joachim.metz[at]gmail[.]com>
```
---------------------------------
Note: this tool and all others in repo - run at your own risk, no warranty implied.

----------------------------------
 ____           ____   __      _       _     
|  _ \ _ __ ___|  _ \ / _| ___| |_ ___| |__  
| |_) | '__/ _ \ | | | |_ / _ \ __/ __| '_ \ 
|  __/| | |  __/ |_| |  _|  __/ || (__| | | |
|_|   |_|  \___|____/|_|  \___|\__\___|_| |_|
                                             

usage: predfetch.py [-h] [-c] [-j] [-n] [-i INPUT] [-o OUTPUT_FILE]

optional arguments:
  -h, --help      show this help message and exit
  -c              Output to CSV
  -j              Output to JSON
  -n              Print to Screen - not pretty
  -i INPUT        Path to Prefetch File(s)
  -o OUTPUT_FILE  Output File Path

----------------------------------
```
Take input of a specific pf file, or directory (will recursively search) and exports to CSV or JSON (sorry I didnt validate the JSON file was valid yet - PR if it isnt). For convenience using Pandas Dataframe - which show allow more flexibility in output. All dates in ISO8601 - truncated volumes to 3 for readability if you have more than that - it will say in  vol_truncated field as true - would recommend modifying the code or using another tool.
ISO8601|GTFO 
