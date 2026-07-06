r"""
utils.py

Description: 
   The purpose of this file is to provide definitions for geo-utility
   functions.

Written by William Chuter-Davies
"""


# Standard Library Imports
import fractions
import math
import pathlib

# Related Third-party Imports
import affine
import numpy
import rasterio
import rasterio.features
import rasterio.transform
import shapely


def create_geometry_mask(geometry:   shapely.geometry.base.BaseGeometry, 
                         resolution: fractions.Fraction) -> tuple[numpy.ndarray, affine.Affine]:
    """
    Create a 2D boolean mask of a
    :class:`shapely.geometry.base.BaseGeometry` at a specified spatial
    resolution.

    Parameters
    ----------
    geometry   : :class:`shapely.geometry.base.BaseGeometry`
        The geometry
    resolution : :class:`fractions.Fraction`
        The spatial resolution

    Returns
    -------
    mask      : :class:`numpy.ndarray`
        A 2D boolean mask
    transform : :class:`affine.Affine`
        A transform mapping array coordinates to world coordinates
    
    Raises
    ------
    ValueError :
        If geometry is empty or produces zero-width or zero-height
        raster at the specified resolution.

    Notes
    -----
    mask is inverted. 
    """
    if geometry.is_empty: 
        raise ValueError('geometry must not be empty')
    
    if resolution == 0: 
        raise ValueError('resolution must not be zero')

    minx, miny, maxx, maxy = geometry.bounds
    width                  = math.ceil((maxx - minx) / resolution)
    height                 = math.ceil((maxy - miny) / resolution)

    if width == 0 or height == 0:
        raise ValueError(f'geometry produces zero-width or zero-height raster at specified resolution: resolution={resolution}')

    transform     = rasterio.transform.from_bounds(minx, 
                                               miny, 
                                               maxx, 
                                               maxy, 
                                               width, 
                                               height)
    geometry_mask = rasterio.features.geometry_mask([geometry], 
                                                (height, width), 
                                                transform, 
                                                invert=True)
    
    return geometry_mask, transform


def write_geometry_mask(geometry_mask: numpy.ndarray, 
                        transform:     affine.Affine, 
                        path:          pathlib.Path) -> None:
    """
    Writes a 2D boolean mask to a GeoTIFF file.

    Parameters
    ----------
    mask      : :class:`numpy.ndarray`
        The 2D boolean mask
    transform : :class:`affine.Affine`
        The transform mapping array coordinates to world coordinates
    path      : :class:`pathlib.Path`
        The path

    Returns
    -------
    None

    Notes
    -----
    CRS set to EPSG:4326. 
    """
    geometry_mask = geometry_mask.astype(numpy.uint8)
    height, width = geometry_mask.shape

    with rasterio.open(path,
                       'w', 
                       'GTiff', 
                       width, 
                       height, 
                       1, 
                       'EPSG:4326', 
                       transform,
                       geometry_mask.dtype) as ds:
        ds.write(geometry_mask, 
                 1)