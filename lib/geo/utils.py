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
import geopandas as gpd
import numpy     as np
import rasterio.features
import rasterio.transform
import shapely.geometry
import shapely.ops
import xarray    as xr

# Local Application/Library Specific Imports
from lib.geo.objects import GeoBoundingBox


# DataArray functions
# ==================================================================================================
def get_da_geometry_as_wkb(
    da: xr.DataArray
) -> bytes:
    """
    Returns the geometry of `da`'s `True` pixels in well-known binary, as a
    MultiPolygon.

    Parameters
    ----------
    da : :class:`xarray.DataArray`
        The boolean mask

    Returns
    -------
    A :class:`bytes`.

    Raises
    ------
    ValueError
        If `da` has fewer than two `lon` or `lat` coordinates, or no `True`
        pixels.
    """
    da   = da.sortby([
        "lon",
        "lat"
    ])
    lons = da["lon"].values
    lats = da["lat"].values

    if len(lons) < 2 or len(lats) < 2:
        raise ValueError("expected `da` to have at least two `lon` and two `lat` coordinates")

    mask = np.flipud(da.values.astype(bool))

    if not mask.any():
        raise ValueError("expected `da` to have at least one `True` pixel")

    half_pixel_lon = (lons.max() - lons.min()) / (len(lons) - 1) / 2
    half_pixel_lat = (lats.max() - lats.min()) / (len(lats) - 1) / 2

    transform = rasterio.transform.from_bounds(
        west   = lons.min() - half_pixel_lon,
        south  = lats.min() - half_pixel_lat,
        east   = lons.max() + half_pixel_lon,
        north  = lats.max() + half_pixel_lat,
        width  = len(lons),
        height = len(lats)
    )

    shapes   = rasterio.features.shapes(
        mask.astype(np.uint8),
        mask      = mask,
        transform = transform
    )
    geometry = shapely.ops.unary_union(
        [
            shapely.geometry.shape(polygon)
            for (
                polygon,
                _
            )
            in shapes
        ]
    )

    if isinstance(geometry, shapely.Polygon):
        geometry = shapely.MultiPolygon([geometry])

    return shapely.to_wkb(geometry)


# ==================================================================================================


# Dataset functions
# ==================================================================================================
def get_ds_variable_coverage(
    ds:       xr.Dataset,
    variable: str,
    mask:     xr.DataArray
) -> float:
    """
    Returns the fraction of `mask`'s pixels with a non-null `variable` value in
    `ds`.

    Parameters
    ----------
    ds : :class:`xarray.Dataset`
        The dataset

    variable : :class:`str`
        The variable id

    mask : :class:`xarray.DataArray`
        The mask

    Returns
    -------
    A :class:`float`.

    Raises
    ------
    ZeroDivisionError
        If `mask` has no `True` values.
    """
    if mask.sum().item() == 0:
        raise ZeroDivisionError("expected `mask` to have at least one `True` value")

    num = (
        ds[variable]
        .notnull()
        .sum()
        .item()
    )
    den = (
        mask
        .sum()
        .item()
    )

    return num / den


def get_ds_variable_mean(
    ds:       xr.Dataset,
    variable: str
) -> float:
    """
    Returns the mean of `variable` for `ds` over dimensions `time`, `lat`, and
    `lon`.

    Parameters
    ----------
    ds : :class:`xarray.Dataset`
        The dataset

    variable : :class:`str`
        The variable id

    Returns
    -------
    A :class:`float`.
    """
    return (
        ds[variable]
        .mean(
            dim    = [
                "time",
                "lat",
                "lon"
            ],
            skipna = True
        )
        .item()
    )


def mask_ds(
    ds:    xr.Dataset,
    masks: list[xr.DataArray]
) -> xr.Dataset:
    """
    Returns `ds` masked by the elementwise `and` of `masks`.

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

    mask = reduce(
        and_,
        masks
    )

    return ds.where(mask)


def select_ds_by_geo_bounding_box(
    ds:               xr.Dataset,
    geo_bounding_box: GeoBoundingBox
) -> xr.Dataset:
    """
    Selects the window of `ds` defined by `geo_bounding_box`.

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


# ==================================================================================================


# GeoDataFrame functions
# ==================================================================================================
def filter_gdf_by_column_membership(
    gdf:    gpd.GeoDataFrame,
    column: str,
    values: list[str]
) -> gpd.GeoDataFrame:
    """
    Filters `gdf` to rows whose `column` value(s) is in `values`.

    Parameters
    ----------
    gdf : :class:`geopandas.GeoDataFrame`
        The geodataframe

    column : :class:`str`
        The column

    values : list[:class:`str`]
        The values

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.
    """
    return gdf[gdf[column].isin(values)]


def join_gdfs_on_within(
    left_gdf:  gpd.GeoDataFrame,
    right_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Joins `left_gdf` to `right_gdf` where `left_gdf` geometries fall within
    `right_gdf` geometries.

    Parameters
    ----------
    left_gdf : :class:`geopandas.GeoDataFrame`
        The left geodataframe

    right_gdf : :class:`geopandas.GeoDataFrame`
        The right geodataframe

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.
    """
    return gpd.sjoin(
        left_df   = left_gdf,
        right_df  = right_gdf,
        predicate = "within"
    )


# ==================================================================================================
