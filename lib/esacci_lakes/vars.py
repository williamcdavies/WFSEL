r"""
vars.py

Description:
    Provides definitions for esacci_lakes-utility variables.

Written by William Chuter-Davies
"""

# Local Application/Library Specific Imports
from lib.esacci_lakes.objects import (
    ESACCILakesVariable,
    HylakField
)

COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND = 7
COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND = 42

ESACCI_LAKES_COVER_CLASS_WATER = 1
ESACCI_LAKES_COVER_CLASS_ICE   = 2
ESACCI_LAKES_COVER_CLASS_CLOUD = 3

ESACCI_LAKES_COVERAGE_LOWER_BOUND = 0.5
ESACCI_LAKES_COVERAGE_UPPER_BOUND = 1.0

ESACCI_LAKES_VARIABLES = {
    "chla":
    ESACCILakesVariable(
        var_id    = "chla",
        long_name = "Concentration of Chlorophyll-a",
        units     = "mg.m-3"
    ),
    "tsm":
    ESACCILakesVariable(
        var_id    = "tsm",
        long_name = "Concentration of Total Suspended Matter",
        units     = "g.m-3"
    ),
    "acdom440":
    ESACCILakesVariable(
        var_id    = "acdom440",
        long_name = "Absorption Coefficient of Coloured Dissolved Organic Matter at 440 nm",
        units     = "m-1"
    ),
    "Kd490":
    ESACCILakesVariable(
        var_id    = "Kd490",
        long_name = "Vertical Diffuse Downwelling Attenuation Coefficient at 490 nm",
        units     = "m-1"
    ),
    "KdPAR":
    ESACCILakesVariable(
        var_id    = "KdPAR",
        long_name = "Vertical Diffuse Downwelling Attenuation Coefficient Aggregated Over PAR",
        units     = "m-1"
    ),
    "phycocyanin":
    ESACCILakesVariable(
        var_id    = "phycocyanin",
        long_name = "Concentration of Phycocyanin Calculated From MDN Algorithm by O'Shea et al. 2021",
        units     = "mg.m-3"
    ),
    "lake_surface_water_temperature":
    ESACCILakesVariable(
        var_id    = "lake_surface_water_temperature",
        long_name = "Lake Surface Skin Temperature",
        units     = "°C"
    ),
    "lake_surface_water_extent":
    ESACCILakesVariable(
        var_id    = "lake_surface_water_extent",
        long_name = "Lake Water Extent",
        units     = "km2"
    )
}

FORMS = [
    "absolute",
    "anomaly"
]

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
        upper_bound   = 500e6
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
        upper_bound   = 5e9
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
        upper_bound   = 20e0
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
        upper_bound   = 500e0
    ),
    "pour_long":
    HylakField(
        field_id      = "pour_long",
        long_name     = "Pour Point Longitude",
        units         = "degrees",
        display_units = "degrees",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = None,
        upper_bound   = None
    ),
    "pour_lat":
    HylakField(
        field_id      = "pour_lat",
        long_name     = "Pour Point Latitude",
        units         = "degrees",
        display_units = "degrees",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = 35e0,
        upper_bound   = 50e0
    )
}

LOCAL_DATA_RUN_DATE = "22-09-26"
