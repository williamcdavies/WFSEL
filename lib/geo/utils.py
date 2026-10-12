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


# GeoDataFrame functions
# ==================================================================================================
def filter_gdf_by_column_membership(
    gdf:    gpd.GeoDataFrame,
    column: str,
    values: list[str]
) -> gpd.GeoDataFrame:
    """
    Filters `gdf` to rows whose `column` values are in `values`.

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
    Joins `left_gdf` to `right_gdf` where `left_gdf` geometries fall
    within `right_gdf` geometries.

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
        left_gdf,
        right_gdf,
        predicate = "within"
    )


# ==================================================================================================


# Dataset functions
# ==================================================================================================
def get_ds_variable_coverage(
    ds:       xr.Dataset,
    variable: str,
    mask:     xr.DataArray
) -> float:
    """
    Returns the fraction of `mask`'s pixels with a non-null `variable`
    value in `ds`.

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
    if (
        mask
        .sum()
        .item()
    ) == 0:
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
    Returns the mean of `variable` for `ds` over dimensions `time`,
    `lat`, and `lon`.

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


def get_geo_bounding_box_from_ds(
    ds: xr.Dataset,
    *,
    lat_max_box: float,
    lat_min_box: float,
    lon_max_box: float,
    lon_min_box: float
) -> GeoBoundingBox:
    """
    Returns the geographic bounding box of `lat_max_box`, `lat_min_box`,
    `lon_max_box` and `lon_min_box`, snapped to the nearest coordinates
    of `ds`.

    Parameters
    ----------
    ds : :class:`xarray.Dataset`
        The dataset

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
            ds["lat"]
            .sel(
                lat    = lat_max_box,
                method = "nearest"
            )
            .item()
        ),
        lat_min = (
            ds["lat"]
            .sel(
                lat    = lat_min_box,
                method = "nearest"
            )
            .item()
        ),
        lon_max = (
            ds["lon"]
            .sel(
                lon    = lon_max_box,
                method = "nearest"
            )
            .item()
        ),
        lon_min = (
            ds["lon"]
            .sel(
                lon    = lon_min_box,
                method = "nearest"
            )
            .item()
        )
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


def select_ds_window_by_geo_bounding_box(
    ds:               xr.Dataset,
    geo_bounding_box: GeoBoundingBox
) -> xr.Dataset:
    """
    Selects the window of `ds` given by `geo_bounding_box`.

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


# DataArray functions
# ==================================================================================================
def get_da_geometry_as_wkb(
    da: xr.DataArray
) -> bytes:
    """
    Returns the geometry of `da`'s `True` pixels in well-known binary.

    Parameters
    ----------
    da : :class:`xarray.DataArray`
        The dataarray

    Returns
    -------
    A :class:`bytes`.

    Raises
    ------
    ValueError
        If `da` has fewer than two `lon` or `lat` coordinates, or no
        `True` pixels.
    """
    da   = da.sortby([
        "lon",
        "lat"
    ])
    lons = da["lon"].values
    lats = da["lat"].values

    if (
        len(lons) < 2 or
        len(lats) < 2
    ):
        raise ValueError("expected `da` to have at least two `lon` and two `lat` coordinates")

    mask = np.flipud(da.values.astype(bool))

    if not mask.any():
        raise ValueError("expected `da` to have at least one `True` pixel")

    pixel_width  = (lons.max() - lons.min()) / (len(lons) - 1)
    pixel_height = (lats.max() - lats.min()) / (len(lats) - 1)

    transform = rasterio.transform.from_bounds(
        west   = lons.min() - (pixel_width  / 2),
        south  = lats.min() - (pixel_height / 2),
        east   = lons.max() + (pixel_width  / 2),
        north  = lats.max() + (pixel_height / 2),
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
