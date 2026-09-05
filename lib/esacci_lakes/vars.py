r"""
vars.py

Description:
   Provides definitions for esacci_lakes-utility variables.

Written by William Chuter-Davies
"""

# Local Application/Library Specific Imports
from lib.esacci_lakes.objects import ESACCILakesVariable

AVERAGE_DEPTH_LOWER_BOUND = 10
AVERAGE_DEPTH_UPPER_BOUND = 50

COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND = 7
COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND = 42

ESACCI_LAKES_VARIABLES = {
    "chla": ESACCILakesVariable(
        "chla",
        "Concentration of Chlorophyll-a",
        "mg.m-3"
    ),
    "tsm": ESACCILakesVariable(
        "tsm",
        "Concentration of Total Suspended Matter",
        "g.m-3"
    ),
    "acdom440": ESACCILakesVariable(
        "acdom440",
        "Absorption Coefficient of Coloured Dissolved Organic Matter at 440 nm",
        "m-1"
    ),
    "Kd490": ESACCILakesVariable(
        "Kd490",
        "Vertical Diffuse Downwelling Attenuation Coefficient at 490 nm",
        "m-1"
    ),
    "KdPAR": ESACCILakesVariable(
        "KdPAR",
        "Vertical Diffuse Downwelling Attenuation Coefficient Aggregated Over PAR",
        "m-1"
    ),
    "phycocyanin": ESACCILakesVariable(
        "phycocyanin",
        "Concentration of Phycocyanin Calculated From MDN Algorithm by O'Shea et al. 2021",
        "mg.m-3"
    ),
    "lake_surface_water_temperature": ESACCILakesVariable(
        "lake_surface_water_temperature",
        "Lake Surface Skin Temperature",
        "˚C"
    ),
    "lake_surface_water_extent": ESACCILakesVariable(
        "lake_surface_water_extent",
        "Lake Water Extent",
        "km2"
    )
}

HYLAK_FIELDS = [
    "lake_name",
    "country",
    "continent",
    "poly_src",
    "lake_type",
    "grand_id",
    "lake_area_m2",
    "shore_len_m",
    "shore_dev",
    "vol_total_m3",
    "vol_res_m3",
    "vol_src",
    "depth_avg_m",
    "dis_avg_m3_per_s",
    "res_time_days",
    "elevation_m",
    "slope_100_m_per_km",
    "wshd_area_m2",
    "pour_long",
    "pour_lat"
]