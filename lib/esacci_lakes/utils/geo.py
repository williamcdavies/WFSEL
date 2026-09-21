r"""
geo.py

Description:
    Provides definitions for esacci_lakes-utility geo functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import xarray as xr

# Local Application/Library Specific Imports
from lib.geo.objects import GeoBoundingBox


def get_geo_bounding_box_from_esacci_lakes_static_lake_mask(
    lat_max_box:                      float,
    lat_min_box:                      float,
    lon_max_box:                      float,
    lon_min_box:                      float,
    esacci_lakes_static_lake_mask_ds: xr.Dataset
) -> GeoBoundingBox:
    """
    Returns a geographic bounding box from `lat_max_box`, `lat_min_box`,
    `lon_max_box`, `lon_min_box`, and an ESA CCI Lakes static lake
    mask.

    Parameters
    ----------
    lat_max_box : :class:`float`
        The northernmost latitude of the bounding box

    lat_min_box : :class:`float`
        The southernmost latitude of the bounding box

    lon_max_box : :class:`float`
        The easternmost longitude of the bounding box

    lon_min_box : :class:`float`
        The westernmost longitude of the bounding box

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    Returns
    -------
    A :class:`lib.geo.objects.GeoBoundingBox`.
    """
    return GeoBoundingBox(
        esacci_lakes_static_lake_mask_ds["lat"]
        .sel(
            lat    = lat_max_box,
            method = "nearest"
        )
        .item(),
        esacci_lakes_static_lake_mask_ds["lat"]
        .sel(
            lat    = lat_min_box,
            method = "nearest"
        )
        .item(),
        esacci_lakes_static_lake_mask_ds["lon"]
        .sel(
            lon    = lon_max_box,
            method = "nearest"
        )
        .item(),
        esacci_lakes_static_lake_mask_ds["lon"]
        .sel(
            lon    = lon_min_box,
            method = "nearest"
        )
        .item()
    )
