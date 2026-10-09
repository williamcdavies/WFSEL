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


# Constants
# ==================================================================================================
COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND = 7
COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND = 42

ESACCI_LAKES_COVER_CLASS_WATER = 1
ESACCI_LAKES_COVER_CLASS_ICE   = 2
ESACCI_LAKES_COVER_CLASS_CLOUD = 3


# ==================================================================================================


# Dictionaries
# ==================================================================================================
ESACCI_LAKES_VARIABLES = {
    "chla":
    ESACCILakesVariable(
        var_id    = "chla",
        long_name = "Concentration of Chlorophyll-a",
        units     = "mg.m3"
    ),
    "tsm":
    ESACCILakesVariable(
        var_id    = "tsm",
        long_name = "Concentration of Total Suspended Matter",
        units     = "g.m3"
    ),
    "acdom440":
    ESACCILakesVariable(
        var_id    = "acdom440",
        long_name = "Absorption Coefficient of Coloured Dissolved Organic Matter at 440 nm",
        units     = "m"
    ),
    "Kd490":
    ESACCILakesVariable(
        var_id    = "Kd490",
        long_name = "Vertical Diffuse Downwelling Attenuation Coefficient at 490 nm",
        units     = "m"
    ),
    "KdPAR":
    ESACCILakesVariable(
        var_id    = "KdPAR",
        long_name = "Vertical Diffuse Downwelling Attenuation Coefficient Aggregated Over PAR",
        units     = "m"
    ),
    "phycocyanin":
    ESACCILakesVariable(
        var_id    = "phycocyanin",
        long_name = "Concentration of Phycocyanin Calculated From MDN Algorithm by O'Shea et al. 2021",
        units     = "mg.m3"
    ),
    "lake_surface_water_temperature":
    ESACCILakesVariable(
        var_id    = "lake_surface_water_temperature",
        long_name = "Lake Surface Skin Temperature",
        units     = "˚C"
    ),
    "lake_surface_water_extent":
    ESACCILakesVariable(
        var_id    = "lake_surface_water_extent",
        long_name = "Lake Water Extent",
        units     = "km2"
    )
}

HYLAK_FIELDS = {
    "hylak_id":
    HylakField(
        field_id      = "hylak_id",
        long_name     = "HydroLAKES ID",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
    ),
    "lake_name":
    HylakField(
        field_id      = "lake_name",
        long_name     = "Lake Name",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
    ),
    "country":
    HylakField(
        field_id      = "country",
        long_name     = "Country",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
    ),
    "continent":
    HylakField(
        field_id      = "continent",
        long_name     = "Continent",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
    ),
    "poly_src":
    HylakField(
        field_id      = "poly_src",
        long_name     = "Polygon Source",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
    ),
    "lake_type":
    HylakField(
        field_id      = "lake_type",
        long_name     = "Lake Type",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
    ),
    "grand_id":
    HylakField(
        field_id      = "grand_id",
        long_name     = "GRanD Reservoir ID",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
    ),
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
    "shore_len_m":
    HylakField(
        field_id      = "shore_len_m",
        long_name     = "Shoreline Length",
        units         = "m",
        display_units = "m",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = None,
        upper_bound   = None
    ),
    "shore_dev":
    HylakField(
        field_id      = "shore_dev",
        long_name     = "Shoreline Development",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
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
    "vol_res_m3":
    HylakField(
        field_id      = "vol_res_m3",
        long_name     = "Reservoir Volume",
        units         = "m3",
        display_units = "m3",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = None,
        upper_bound   = None
    ),
    "vol_src":
    HylakField(
        field_id      = "vol_src",
        long_name     = "Volume Source",
        units         = "",
        display_units = "",
        scale         = None,
        display_scale = None,
        lower_bound   = None,
        upper_bound   = None
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
    "dis_avg_m3_per_s":
    HylakField(
        field_id      = "dis_avg_m3_per_s",
        long_name     = "Average Discharge",
        units         = "m3.s",
        display_units = "m3.s",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = None,
        upper_bound   = None
    ),
    "res_time_days":
    HylakField(
        field_id      = "res_time_days",
        long_name     = "Residence Time",
        units         = "days",
        display_units = "days",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = None,
        upper_bound   = None
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
    "slope_100_m_per_km":
    HylakField(
        field_id      = "slope_100_m_per_km",
        long_name     = "Shoreline Slope",
        units         = "m.km",
        display_units = "m.km",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = None,
        upper_bound   = None
    ),
    "wshd_area_m2":
    HylakField(
        field_id      = "wshd_area_m2",
        long_name     = "Watershed Area",
        units         = "m2",
        display_units = "m2",
        scale         = 1e0,
        display_scale = 1e0,
        lower_bound   = None,
        upper_bound   = None
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


# ==================================================================================================
