r"""
utils.py

Description: 
   The purpose of this file is to provide definitions for utility and
   utility-like functions.

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


def get_geometry_mask(geometry:   shapely.geometry.base.BaseGeometry, 
                      resolution: fractions.Fraction) -> tuple[numpy.ndarray, affine.Affine]:
    """
    Create a 2D boolean mask of a
    :class:`shapely.geometry.base.BaseGeometry` at a specified spatial
    resolution.

    Parameters
    ----------
    geometry   : :class:`shapely.geometry.base.BaseGeometry`
        Geometry
    resolution : :class:`fractions.Fraction`
        Spatial resolution

    Returns
    -------
    geometry_mask : :class:`numpy.ndarray`
        2D boolean mask
    transform     : :class:`affine.Affine`
        Affine transform mapping array coordinates to world coordinates
    
    Raises
    ------
    ValueError :
        If geometry is empty or if it produces a zero-width or
        zero-height raster at the specified resolution.
    """
    if geometry.is_empty: 
        raise ValueError("cannot create geometry mask from empty geometry")

    minx, miny, maxx, maxy = geometry.bounds
    width                  = math.ceil((maxx - minx) / resolution)
    height                 = math.ceil((maxy - miny) / resolution)

    if width == 0 or height == 0:
        raise ValueError("geometry produces zero-width or zero-height raster at this resolution")

    transform              = rasterio.transform.from_bounds(minx, 
                                                            miny, 
                                                            maxx, 
                                                            maxy, 
                                                            width, 
                                                            height)
    geometry_mask          = rasterio.features.geometry_mask([geometry], 
                                                             (height, width), 
                                                             transform, 
                                                             invert=True)
    
    return geometry_mask, transform