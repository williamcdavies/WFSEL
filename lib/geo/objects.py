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
    Dataclass object for representing a bounding box.
    """

    lat_max: float
    lat_min: float
    lon_max: float
    lon_min: float
