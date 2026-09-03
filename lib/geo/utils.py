r"""
utils.py

Description:
   Provides definitions for geo-utility functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import geopandas  as gpd
import sqlalchemy
import xarray     as xr

# Local Application/Library Specific Imports
from lib.geo.objects import GeoBoundingBox


def sel(
    ds:               xr.Dataset,
    geo_bounding_box: GeoBoundingBox
) -> xr.Dataset:
    """
    Selects a window from an :class:`xarray.Dataset` whose bounds is
    defined by :class:`GeoBoundingBox.lat_min`,
    :class:`GeoBoundingBox.lat_max`, :class:`GeoBoundingBox.lon_min`,
    and :class:`GeoBoundingBox.lon_max`.

    Parameters
    ----------
    ds : :class:`xarray.Dataset`
        The :class:`xarray.Dataset`

    geo_bounding_box : :class:`GeoBoundingBox`
        The :class:`GeoBoundingBox`

    Returns
    -------
    A :class:`xarray.Dataset`.
    """
    return ds.sel(
        lat=slice(
            geo_bounding_box.lat_min,
            geo_bounding_box.lat_max
        ),
        lon=slice(
            geo_bounding_box.lon_min,
            geo_bounding_box.lon_max
        )
    )


def get_gdf_from_postgis(
    query:      str,
    connection: sqlalchemy.Connection
) -> gpd.GeoDataFrame:
    """
    Get a :class:`geopandas.GeoDataFrame` from a query and a
    :class:`sqlalchemy.Connection`.

    Parameters
    ----------
    query : :class:`str`
        The query

    connection : :class:`sqlalchemy.Connection`
        The connection

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.

    Notes
    -----
    Internal `geopandas.read_postgis` call assumes geom_col="geom".
    """
    return gpd.read_postgis(
        query,
        connection
    )


def join_gdfs_on_within(
    left_gdf:  gpd.GeoDataFrame,
    right_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Returns a :class:`geopandas.GeoDataFrame` of `left_gdf` joined with
    `right_gdf` where each `left_gdf` geometry is within a corresponding
    `right_gdf` geometry.

    Parameters
    ----------
    left_gdf : :class:`geopandas.GeoDataFrame`
        The left :class:`geopandas.GeoDataFrame`

    right_gdf : :class:`geopandas.GeoDataFrame`
        The right :class:`geopandas.GeoDataFrame`

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.
    """
    return gpd.sjoin(
        left_df=left_gdf,
        right_df=right_gdf,
        predicate="within"
    )