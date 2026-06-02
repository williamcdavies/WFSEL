"""
printshp.py

The purpose of this prorgam is to print Shapefile metadata to `sys.stdout`.

Usage: python printshp.py <shp_path>

Example:

```sh
$ python printshp.py /Users/username/Downloads/lakes_cci_v2.1.0_shp/lakescci_v2.1.0_data-availability.shp
shapefile Reader
    2024 shapes (type 'POLYGON')
    2024 records (18 fields)
```

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

# Third-Party Imports
import shapefile

filename = sys.argv[1]
sf       = shapefile.Reader(filename)

print(sf)