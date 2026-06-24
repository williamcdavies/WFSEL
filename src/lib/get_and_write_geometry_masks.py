r"""
get_and_write_geometry_masks.py

Description: 
    The purpose of this program is to pre-compute and write, for each
    feature in the attribute table of a Shapefile, a geometry mask for
    application against netCDF files of a common coordinate reference
    system (CRS) and spatial resolution.

Usage: 
    python get_and_write_geometry_masks.py <shp_path> <dst_path>

Example:
    ```sh
    python get_and_write_geometry_masks.py ~/Downloads/WFSEL/ESA/lakes_cci_v2.1.0_shp ~/Downloads/WFSEL/ESA/masks
    ```

Notes:
    If the Shapefile has no assigned CRS, EPSG:4326 will be assigned. If
    the Shapefile has an assigned CRS, it will be projected into
    EPSG:4326.

Written by William Chuter-Davies
"""


# Standard Library Imports
import fractions
import pathlib
import sys

# Related Third-party Imports
import geopandas

# Local Application/Library Specific Imports
from lib.utils import get_geometry_mask, write_geometry_mask


# Global Definitions
RETURN_SUCCESS = 0
RETURN_FAILURE = 1


def main() -> int:
    # If argument count is not equal to 3, return with `RETURN_FAILURE`
    if len(sys.argv) != 3:
        print(f'fatal: unexpected argument count: {sys.argv}')
        
        return RETURN_FAILURE

    # For each path in `sys.argv` build corresponding Path and read into
    # `paths`
    paths = [pathlib.Path(p) for p in sys.argv[1:3]]
   
    # For each path in `paths` ...
    for path in paths:
        # If path does not exist, return with `RETURN_FAILURE`
        if not path.exists():
            print(f'fatal: no such file or directory: {path}')
         
            return RETURN_FAILURE

    # Read `paths` into `shp_path` and `dst_path`
    shp_path, dst_path = paths

    # Attempt to ...
    try:
        # Open GeoDataFrame specified by `shp_path`
        gdf = geopandas.read_file(shp_path)
    # On exception, return with `RETURN_FAILURE`
    except Exception as e:
        print(f'fatal: exception: {e}')
        
        return RETURN_FAILURE

    # Ensure `gdf` is in EPSG:4326
    if gdf.crs is None:
        gdf = gdf.set_crs('EPSG:4326')
    else:
        gdf = gdf.to_crs('EPSG:4326')

    # Read `gdf.active_geometry_name` into `active_geometry_name`
    active_geometry_name = gdf.active_geometry_name

    # If `active_geometry_name` is None, return with `RETURN_FAILURE`
    if active_geometry_name is None:
        print('fatal: GeoDataFrame has no active geometry name')

        return RETURN_FAILURE

    # For each row in `gdf` ...
    for _, data in gdf.iterrows():
        # Build `geometry_mask` and `transform` from `data`
        geometry_mask, transform = get_geometry_mask(data[active_geometry_name], 
                                                     fractions.Fraction(1, 
                                                                        120))
        
        # Write `geometry_mask` and `transform` to `dst_path`
        write_geometry_mask(geometry_mask, 
                            transform, 
                            dst_path / f'{data['id']}.tif')
    
    return RETURN_SUCCESS


if __name__ == '__main__':
    sys.exit(main())