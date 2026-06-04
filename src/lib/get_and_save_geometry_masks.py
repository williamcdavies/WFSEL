r"""
get_and_save_geometry_masks.py

Description: 
    The purpose of this program is to pre-compute and save, for each
    feature in the attribute table of a Shapefile, a geometry mask for
    application against netCDF files of a common coordinate reference
    system (CRS) and spatial resolution.

Usage: 
    python get_and_save_geometry_masks.py <shp_path>

Example:
    ```sh
    ```

Written by William Chuter-Davies
"""


# Standard Library Imports
import fractions
import pathlib
import sys

# Related Third-party Imports
import geopandas

# Local Application/Library Specific Imports
from lib.utils import get_geometry_mask


# Global Definitions
RETURN_SUCCESS = 0
RETURN_FAILURE = 1


def main() -> int:
    # If argument count is not equal to 2, return with `RETURN_FAILURE`
    if len(sys.argv) != 2:
        print(f"fatal: unexpected argument count: {sys.argv}")
        
        return RETURN_FAILURE

    # Read `sys.argv[1]` into `shp_path`
    shp_path = pathlib.Path(sys.argv[1])
    
    # If `shp_path` does not exist, return with `RETURN_FAILURE`
    if not shp_path.exists():
        print(f"fatal: no such file or directory: {sys.argv[1]}")

        return RETURN_FAILURE

    # Attempt to ...
    try:
        # ... open GeoDataFrame specified by `shp_path`
        gdf = geopandas.read_file(shp_path)
    # On exception, return with `RETURN_FAILURE`
    except Exception as e:
        print(f"fatal: exception: {e}")
        
        return RETURN_FAILURE

    # Ensure `gdf` is in EPSG:4326
    if gdf.crs is None:
        gdf = gdf.set_crs('epsg:4326')
    else:
        gdf = gdf.to_crs('epsg:4326')

    # Read `gdf.active_geometry_name` into `active_geometry_name`
    active_geometry_name = gdf.active_geometry_name

    # If `active_geometry_name` is None, return with `RETURN_FAILURE`
    if active_geometry_name is None:
        print("fatal: GeoDataFrame has no active geometry name")

        return RETURN_FAILURE

    for index, data in gdf.iterrows():
        geometry_mask = get_geometry_mask(data[active_geometry_name], fractions.Fraction(1, 120))
    
    return RETURN_SUCCESS


if __name__ == '__main__':
    sys.exit(main())