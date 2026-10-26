"""
wfsel.geo.models.

Written by William Chuter-Davies
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
