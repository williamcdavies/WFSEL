"""
printnc.py

The purpose of this prorgam is to print netCDF metadata to `sys.stdout`.

Usage: python printnc.py <nc_path>

Example:

```sh
$ python printnc.py /Users/username/Downloads/ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20230101-fv3.0.0.nc 
<class 'netCDF4.Dataset'>
.
.
.
groups:
```

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

# Third-Party Imports
from netCDF4 import Dataset

filename = sys.argv[1]
rootgrp  = Dataset(filename)

print(rootgrp)

rootgrp.close()