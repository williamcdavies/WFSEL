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
        The ESA CCI Lakes static lake mask

    Returns
    -------
    A :class:`GeoBoundingBox`.

    Raises
    ------
    AttributeError
        If `esacci_lakes_metadata` does not have `lat_max_box`,
        `lat_min_box`, `lon_max_box`, and `lon_min_box` attributes.

    Notes
    -----
    Assumes `esacci_lakes_metadata` has `lat_max_box`, `lat_min_box`,
    `lon_max_box`, and `lon_min_box` attributes.
    """
    for attribute in ("lat_max_box", "lat_min_box", "lon_max_box", "lon_min_box"):
        if not hasattr(esacci_lakes_metadata, attribute):
            raise AttributeError(f"expected `esacci_lakes_metadata` to have a \"{attribute}\" attribute")

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
