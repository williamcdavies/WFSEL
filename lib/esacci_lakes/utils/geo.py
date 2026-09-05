r"""
geo.py

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


def get_geo_bounding_box_from_static_lake_mask(
    esacci_lakes_metadata:            Any,
    esacci_lakes_static_lake_mask_ds: xr.Dataset
) -> GeoBoundingBox:
    """
    Get a geographic bounding box from ESA CCI Lakes metadata and an ESA
    CCI Lakes static lake mask.

    Parameters
    ----------
    esacci_lakes_metadata : Any
        The ESA CCI Lakes metadata

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes stataic lake mask

    Returns
    -------
    A :class:`GeoBoundingBox`.
    """
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
