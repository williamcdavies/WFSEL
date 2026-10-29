"""
Filename:   wfsel.geo.models.py
Author:     William Chuter-Davies
Modified:   29/10/26
"""

# Standard Library Imports
from dataclasses import dataclass


@dataclass(kw_only = True)
class GeographicBoundingBox:
    """Encapsulate a GeographicBoundingBox."""

    lat_max:    float
    lat_min:    float
    lon_max:    float
    lon_min:    float
