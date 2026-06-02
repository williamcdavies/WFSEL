"""
printshp.py

Description:
    The purpose of this prorgam is to print Shapefile metadata to
    `sys.stdout`.

Usage: 
    python printshp.py <shp_path>

Example:
    ```sh
    $ python src/lib/printshp.py /Users/williamchuter-davies/Downloads/WFEL/ESA/lakes_cci_v2.1.0_shp/lakescci_v2.1.0_data-availability.shp
                id    short_name              name lat_centre  ... lic_data lwlr_data  type                                           geometry
    0             2  GLWD00000002          Superior    47,9625  ...        0         0  Lake  MULTIPOLYGON (((-92.27778 46.65417, -92.27223 ...
    1             3  GLWD00000003          Victoria    -0,8764  ...        0         0  Lake  MULTIPOLYGON (((31.6986 -0.85555, 31.6986 -0.8...
    2             4  GLWD00000004    Large Aral Sea    44,6486  ...        0         0  Lake  MULTIPOLYGON (((58.43471 44.31667, 58.43332 44...
    3             5  GLWD00000005             Huron    44,7208  ...        0         0  Lake  MULTIPOLYGON (((-84.37778 45.98056, -84.37223 ...
    4             6  GLWD00000006          Michigan    42,6042  ...        0         0  Lake  MULTIPOLYGON (((-87.98334 44.66389, -87.98334 ...
    ...         ...           ...               ...        ...  ...      ...       ...   ...                                                ...
    2019  300134644  HYLA00134644        Rihpojávri    69,2125  ...        0         0  Lake  MULTIPOLYGON (((20.59582 69.22917, 20.5986 69....
    2020  300136326  HYLA00136326              None    68,8208  ...        0         0  Lake  POLYGON ((59.04026 68.84306, 59.04026 68.84167...
    2021  300140744  HYLA00140744              None    67,4625  ...        0         0  Lake  POLYGON ((49.86249 67.48056, 49.86249 67.47917...
    2022  300164228  HYLA00164228              None    53,3792  ...        0         0  Lake  POLYGON ((58.66387 53.39028, 58.66387 53.38889...
    2023  300165102  HYLA00165102  Großer Müggelsee    52,4375  ...        0         0  Lake  POLYGON ((13.62504 52.44445, 13.63193 52.44445...

    [2024 rows x 18 columns]
    ```

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from pathlib import Path

# Third-Party Imports
import geopandas

# Read `sys.argv[1]` into `shp_path`
shp_path = Path(sys.argv[1])

# Assert `shp_path.exists()`
assert shp_path.exists()

# Read `shp_path` into GeoDataFrame
gdf = geopandas.read_file(shp_path)

# Print GeoDataFrame
print(gdf)