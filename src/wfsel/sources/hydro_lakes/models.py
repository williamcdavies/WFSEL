"""wfsel.sources.hydro_lakes.models.

Written by William Chuter-Davies
"""

# Standard Library Imports
from dataclasses import dataclass


@dataclass(kw_only = True)
class HylakField:
    """Encapsulates HylakField."""

    field_id:      str
    long_name:     str
    units:         str
    display_units: str
    scale:         float | None
    display_scale: float | None
    lower_bound:   float | None
    upper_bound:   float | None


HYLAK_FIELDS = {
    "lake_area_m2":
    HylakField(
        field_id      = "lake_area_m2",
        long_name     = "Lake Area",
        units         = "m2",
        display_units = "km2",
        scale         = 1e0,
        display_scale = 1e6,
        lower_bound   = 100e6,
        upper_bound   = 500e6,
    ),
    "vol_total_m3":
    HylakField(
        field_id      = "vol_total_m3",
        long_name     = "Total Lake Volume",
        units         = "m3",
        display_units = "km3",
        scale         = 1e0,
        display_scale = 1e9,
        lower_bound   = 0.5e9,
        upper_bound   = 5e9,
    ),
    "depth_avg_m":
    HylakField(
        field_id      = "depth_avg_m",
        long_name     = "Average Depth",
        units         = "m",
        display_units = "m",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = 5e0,
        upper_bound   = 20e0,
    ),
    "elevation_m":
    HylakField(
        field_id      = "elevation_m",
        long_name     = "Elevation",
        units         = "m",
        display_units = "m",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = 100e0,
        upper_bound   = 500e0,
    ),
    "pour_long_deg":
    HylakField(
        field_id      = "pour_long_deg",
        long_name     = "Pour Point Longitude",
        units         = "degrees",
        display_units = "degrees",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = None,
        upper_bound   = None,
    ),
    "pour_lat_deg":
    HylakField(
        field_id      = "pour_lat_deg",
        long_name     = "Pour Point Latitude",
        units         = "degrees",
        display_units = "degrees",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = 35e0,
        upper_bound   = 50e0,
    ),
}
