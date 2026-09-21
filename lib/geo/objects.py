r"""
objects.py

Description:
    Provides definitions for geo-utility classes.

Written by William Chuter-Davies
"""

# Standard Library Imports
from dataclasses import dataclass


@dataclass
class GeoBoundingBox:
    """
    Dataclass object for representing a geographic bounding box.

    Parameters
    ----------
    lat_max : :class:`float`
        The northernmost latitudinal measurement

    lat_min : :class:`float`
        The southernmost latitudinal measurement

    lon_max : :class:`float`
        The easternmost longitudinal measurement

    lon_min : :class:`float`
        The westernmost longitudinal measurement
    """
    lat_max: float
    lat_min: float
    lon_max: float
    lon_min: float
