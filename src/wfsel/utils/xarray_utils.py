"""
Filename:   wfsel.utils.xarray_utils.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Related Third-party Imports
import xarray as xr

# Local Application/Library Specific Imports
from wfsel.geo.models import GeographicBoundingBox


def build_geographic_bounding_box(
    ds: xr.Dataset,
    *,
    lat_max:    float,
    lat_min:    float,
    lon_max:    float,
    lon_min:    float,
) -> GeographicBoundingBox:
    """
    Build a geographic bounding box.

    Parameters
    ----------
    ds : xr.Dataset
        The dataset
    lat_max : float
        The maximum latitude
    lat_min : float
        The minimum latitude
    lon_max : float
        The maximum longitude
    lon_min : float
        The minimum longitude

    Returns
    -------
    GeographicBoundingBox
        A geographic bounding box
    """
    lat_max = float(
                ds["lat"]
                .sel(
                    lat     = lat_max,
                    method  = "nearest",
                ),
            )
    lat_min = float(
                ds["lat"]
                .sel(
                    lat     = lat_min,
                    method  = "nearest",
                ),
            )
    lon_max = float(
                ds["lon"]
                .sel(
                    lon     = lon_max,
                    method  = "nearest",
                ),
            )
    lon_min = float(
                ds["lon"]
                .sel(
                    lon     = lon_min,
                    method  = "nearest",
                ),
            )

    bbox    = GeographicBoundingBox(
                lat_max = lat_max,
                lat_min = lat_min,
                lon_max = lon_max,
                lon_min = lon_min,
            )

    return bbox


def window(
    ds:                      xr.Dataset,
    geographic_bounding_box: GeographicBoundingBox,
) -> xr.Dataset:
    """
    Window a dataset by a geographic bounding box.

    Parameters
    ----------
    ds : xr.Dataset
        The dataset
    geographic_bounding_box : GeographicBoundingBox
        The geographic bounding box

    Returns
    -------
    xr.Dataset
        A dataset
    """
    window  = ds.sel(
                lat = slice(
                    geographic_bounding_box.lat_min,
                    geographic_bounding_box.lat_max,
                ),
                lon = slice(
                    geographic_bounding_box.lon_min,
                    geographic_bounding_box.lon_max,
                ),
            )

    return window


def compute_spatial_mean(
    da: xr.DataArray,
) -> float:
    """
    Compute the spatial mean of a dataarray.

    Parameters
    ----------
    da : xr.DataArray
        The dataarray

    Returns
    -------
    float
        A spatial mean
    """
    spatial_mean = float(
                    da
                    .mean(
                        [
                            "lat",
                            "lon",
                            "time",
                        ],
                    )
                    .item(),
                )

    return spatial_mean


def compute_spatial_coverage(
    numerator_mask:   xr.DataArray,
    denominator_mask: xr.DataArray,
) -> float:
    """
    Compute the spatial coverage of a dataset.

    Parameters
    ----------
    numerator_mask : xr.DataArray
        The numerator mask
    denominator_mask : xr.DataArray
        The denominator mask

    Returns
    -------
    float
        A spatial coverage

    Raises
    ------
    TypeError
        If the numerator mask is not of dtype bool
    TypeError
        If the denominator mask is not of dtype bool
    """
    if numerator_mask.dtype != bool:
        message = f"expected numerator mask to be of dtype bool: got {numerator_mask.dtype}"

        raise TypeError(message)

    if denominator_mask.dtype != bool:
        message = f"expected denominator mask to be of dtype bool: got {denominator_mask.dtype}"

        raise TypeError(message)

    numerator_sum   = int(
                        numerator_mask
                        .sum()
                        .item(),
                    )
    denominator_sum = int(
                        denominator_mask
                        .sum()
                        .item(),
                    )

    if denominator_sum == 0:
        spatial_coverage = float("nan")
    else:
        spatial_coverage    = (
                                numerator_sum /
                                denominator_sum
                            )

    return spatial_coverage
