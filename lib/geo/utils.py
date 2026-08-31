r"""
utils.py

Description:
   Provides definitions for geo-utility functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import xarray as xr

# Local Application/Library Specific Imports
from lib.geo.objects import GeoBoundingBox


def sel(
    ds: xr.Dataset,
    geo_bounding_box: GeoBoundingBox,
) -> xr.Dataset:
    return ds.sel(
        lat=slice(
            geo_bounding_box.lat_min,
            geo_bounding_box.lat_max,
        ),
        lon=slice(
            geo_bounding_box.lon_min,
            geo_bounding_box.lon_max,
        ),
    )
