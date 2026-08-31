r"""
utils.py

Description:
   Provides definitions for esacci_lakes-utility geo functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from typing import Any

# Related Third-party Imports
import xarray as xr

# Local Application/Library Specific Imports
from lib.geo.objects import GeoBoundingBox


def get_geo_bounding_box(
    esacci_lakes_metadata: Any,
    esacci_lakes_static_lake_mask_ds: xr.Dataset
) -> GeoBoundingBox:
    return GeoBoundingBox(
        esacci_lakes_static_lake_mask_ds["lat"]
        .sel(
            lat=esacci_lakes_metadata.lat_max_box,
            method="nearest"
        )
        .item(),
        esacci_lakes_static_lake_mask_ds["lat"]
        .sel(
            lat=esacci_lakes_metadata.lat_min_box,
            method="nearest"
        )
        .item(),
        esacci_lakes_static_lake_mask_ds["lon"]
        .sel(
            lon=esacci_lakes_metadata.lon_max_box,
            method="nearest"
        )
        .item(),
        esacci_lakes_static_lake_mask_ds["lon"]
        .sel(
            lon=esacci_lakes_metadata.lon_min_box,
            method="nearest"
        )
        .item()
    )
