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


# Bounding box functions
# ==================================================================================================
def get_geo_bounding_box_from_esacci_lakes_static_lake_mask(
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
    *,
    lat_max_box: float,
    lat_min_box: float,
    lon_max_box: float,
    lon_min_box: float
) -> GeoBoundingBox:
    """
    Returns the geographic bounding box of `lat_max_box`, `lat_min_box`,
    `lon_max_box` and `lon_min_box`, snapped to the nearest coordinates of
    `esacci_lakes_static_lake_mask_ds`.

    Parameters
    ----------
    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    lat_max_box : :class:`float`
        The northernmost latitude of the bounding box

    lat_min_box : :class:`float`
        The southernmost latitude of the bounding box

    lon_max_box : :class:`float`
        The easternmost longitude of the bounding box

    lon_min_box : :class:`float`
        The westernmost longitude of the bounding box

    Returns
    -------
    A :class:`lib.geo.objects.GeoBoundingBox`.
    """
    return GeoBoundingBox(
        lat_max = (
            esacci_lakes_static_lake_mask_ds["lat"]
            .sel(
                lat    = lat_max_box,
                method = "nearest"
            )
            .item()
        ),
        lat_min = (
            esacci_lakes_static_lake_mask_ds["lat"]
            .sel(
                lat    = lat_min_box,
                method = "nearest"
            )
            .item()
        ),
        lon_max = (
            esacci_lakes_static_lake_mask_ds["lon"]
            .sel(
                lon    = lon_max_box,
                method = "nearest"
            )
            .item()
        ),
        lon_min = (
            esacci_lakes_static_lake_mask_ds["lon"]
            .sel(
                lon    = lon_min_box,
                method = "nearest"
            )
            .item()
        )
    )


# ==================================================================================================


# Mask functions
# ==================================================================================================
def get_esacci_lakes_cover_class_mask(
    esacci_lakes_cover_class:       int,
    esacci_lakes_merged_product_ds: xr.Dataset
) -> xr.DataArray:
    """
    Returns a boolean mask of `esacci_lakes_merged_product_ds`'s
    "lake_cover_class" pixels equal to `esacci_lakes_cover_class`.

    Parameters
    ----------
    esacci_lakes_cover_class : :class:`int`
        One of `ESACCI_LAKES_COVER_CLASS_WATER`, `ESACCI_LAKES_COVER_CLASS_ICE`,
        or `ESACCI_LAKES_COVER_CLASS_CLOUD`

    esacci_lakes_merged_product_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes merged product

    Returns
    -------
    A :class:`xarray.DataArray`.
    """
    return esacci_lakes_merged_product_ds["lake_cover_class"] == esacci_lakes_cover_class


def get_esacci_lakes_id_mask(
    esacci_lakes_id:                  int,
    esacci_lakes_static_lake_mask_ds: xr.Dataset
) -> xr.DataArray:
    """
    Returns a boolean mask of `esacci_lakes_static_lake_mask_ds`'s "CCI_lakeid"
    pixels equal to `esacci_lakes_id`.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    Returns
    -------
    A :class:`xarray.DataArray`.
    """
    return esacci_lakes_static_lake_mask_ds["CCI_lakeid"] == esacci_lakes_id


# ==================================================================================================
