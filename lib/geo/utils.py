r"""
utils.py

Description:
    Provides definitions for geo-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from functools import reduce
from operator  import and_

# Related Third-party Imports
import geopandas  as gpd
import xarray     as xr

# Local Application/Library Specific Imports
from lib.geo.objects import GeoBoundingBox


def select_ds_by_geo_bounding_box(
    ds:               xr.Dataset,
    geo_bounding_box: GeoBoundingBox
) -> xr.Dataset:
    """
    Selects the window of `ds` within `geo_bounding_box`.

    Parameters
    ----------
    ds : :class:`xarray.Dataset`
        The dataset

    geo_bounding_box : :class:`lib.geo.objects.GeoBoundingBox`
        The bounding box

    Returns
    -------
    A :class:`xarray.Dataset`.
    """
    return ds.sel(
        lat = slice(
            geo_bounding_box.lat_min,
            geo_bounding_box.lat_max
        ),
        lon = slice(
            geo_bounding_box.lon_min,
            geo_bounding_box.lon_max
        )
    )


def mask_ds_by_combined_masks(
    ds:    xr.Dataset,
    masks: list[xr.DataArray]
) -> xr.Dataset:
    """
    Returns `ds` masked by the elementwise `&` of `masks`.

    Parameters
    ----------
    ds : :class:`xarray.Dataset`
        The dataset

    masks : list[:class:`xarray.DataArray`]
        The masks

    Returns
    -------
    A :class:`xarray.Dataset`.

    Raises
    ------
    ValueError
        If `masks` is empty.
    """
    if not masks:
        raise ValueError("expected `masks` to be non-empty")

    mask = reduce(and_, masks)

    return ds.where(mask)


def join_gdfs_on_within(
    left_gdf:  gpd.GeoDataFrame,
    right_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Joins `left_gdf` to `right_gdf` where `left_gdf` geometries fall
    within `right_gdf` geometries.

    Parameters
    ----------
    left_gdf : :class:`geopandas.GeoDataFrame`
        The left dataframe

    right_gdf : :class:`geopandas.GeoDataFrame`
        The right dataframe

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.
    """
    return gpd.sjoin(
        left_df   = left_gdf,
        right_df  = right_gdf,
        predicate = "within"
    )
