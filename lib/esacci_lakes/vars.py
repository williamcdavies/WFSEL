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

ESACCI_LAKES_VARIABLES = {
    "chla": ESACCILakesVariable(
        "chla",
        "Concentration of Chlorophyll-a",
        "mg.m3"
    ),
    "tsm": ESACCILakesVariable(
        "tsm",
        "Concentration of Total Suspended Matter",
        "g.m3"
    ),
    "acdom440": ESACCILakesVariable(
        "acdom440",
        "Absorption Coefficient of Coloured Dissolved Organic Matter at 440 nm",
        "m"
    ),
    "Kd490": ESACCILakesVariable(
        "Kd490",
        "Vertical Diffuse Downwelling Attenuation Coefficient at 490 nm",
        "m"
    ),
    "KdPAR": ESACCILakesVariable(
        "KdPAR",
        "Vertical Diffuse Downwelling Attenuation Coefficient Aggregated Over PAR",
        "m"
    ),
    "phycocyanin": ESACCILakesVariable(
        "phycocyanin",
        "Concentration of Phycocyanin Calculated From MDN Algorithm by O'Shea et al. 2021",
        "mg.m3"
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

HYLAK_FIELDS = {
    "lake_name": HylakField(
        "lake_name",
        "Lake Name",
        "",
        None,
        None
    ),
    "country": HylakField(
        "country",
        "Country",
        "",
        None,
        None
    ),
    "continent": HylakField(
        "continent",
        "Continent",
        "",
        None,
        None
    ),
    "poly_src": HylakField(
        "poly_src",
        "Polygon Source",
        "",
        None,
        None
    ),
    "lake_type": HylakField(
        "lake_type",
        "Lake Type",
        "",
        None,
        None
    ),
    "grand_id": HylakField(
        "grand_id",
        "GRanD Reservoir ID",
        "",
        None,
        None
    ),
    "lake_area_m2": HylakField(
        "lake_area_m2",
        "Lake Area",
        "m2",
        50e6,
        500e6
    ),
    "shore_len_m": HylakField(
        "shore_len_m",
        "Shoreline Length",
        "m-1",
        None,
        None
    ),
    "shore_dev": HylakField(
        "shore_dev",
        "Shoreline Development",
        "",
        None,
        None
    ),
    "vol_total_m3": HylakField(
        "vol_total_m3",
        "Total Lake Volume",
        "m3",
        0.5e9,
        5e9
    ),
    "vol_res_m3": HylakField(
        "vol_res_m3",
        "Reservoir Volume",
        "m3",
        None,
        None
    ),
    "vol_src": HylakField(
        "vol_src",
        "Volume Source",
        "",
        None,
        None
    ),
    "depth_avg_m": HylakField(
        "depth_avg_m",
        "Average Depth",
        "m",
        5,
        20
    ),
    "dis_avg_m3_per_s": HylakField(
        "dis_avg_m3_per_s",
        "Average Discharge",
        "m3.s",
        None,
        None
    ),
    "res_time_days": HylakField(
        "res_time_days",
        "Residence Time",
        "days",
        None,
        None
    ),
    "elevation_m": HylakField(
        "elevation_m",
        "Elevation",
        "m",
        100,
        500
    ),
    "slope_100_m_per_km": HylakField(
        "slope_100_m_per_km",
        "Shoreline Slope",
        "m.km",
        None,
        None
    ),
    "wshd_area_m2": HylakField(
        "wshd_area_m2",
        "Watershed Area",
        "m2",
        None,
        None
    ),
    "pour_long": HylakField(
        "pour_long",
        "Pour Point Longitude",
        "degrees",
        None,
        None
    ),
    "pour_lat": HylakField(
        "pour_lat",
        "Pour Point Latitude",
        "degrees",
        20,
        40
    )
}