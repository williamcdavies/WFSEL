r"""
geo.py

Description:
    Provides definitions for esacci_lakes-utility geo functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import xarray as xr


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
        One of `ESACCI_LAKES_COVER_CLASS_WATER`,
        `ESACCI_LAKES_COVER_CLASS_ICE`, or
        `ESACCI_LAKES_COVER_CLASS_CLOUD`

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
    Returns a boolean mask of `esacci_lakes_static_lake_mask_ds`'s
    "CCI_lakeid" pixels equal to `esacci_lakes_id`.

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
