"""wfsel.sources.esacci_lakes.models.

Written by William Chuter-Davies
"""

# Standard Library Imports
from dataclasses import dataclass


@dataclass(kw_only = True)
class ESACCILakesVariable:
    """Encapsulates ESACCILakesVariable."""

    var_id:    str
    long_name: str
    units:     str


ESACCI_LAKES_VARIABLES = {
    "chla":
    ESACCILakesVariable(
        var_id    = "chla",
        long_name = "Concentration of Chlorophyll-a",
        units     = "mg.m-3",
    ),
    "tsm":
    ESACCILakesVariable(
        var_id    = "tsm",
        long_name = "Concentration of Total Suspended Matter",
        units     = "g.m-3",
    ),
    "acdom440":
    ESACCILakesVariable(
        var_id    = "acdom440",
        long_name = "Absorption Coefficient of Coloured Dissolved Organic Matter at 440 nm",
        units     = "m-1",
    ),
    "Kd490":
    ESACCILakesVariable(
        var_id    = "Kd490",
        long_name = "Vertical Diffuse Downwelling Attenuation Coefficient at 490 nm",
        units     = "m-1",
    ),
    "KdPAR":
    ESACCILakesVariable(
        var_id    = "KdPAR",
        long_name = "Vertical Diffuse Downwelling Attenuation Coefficient Aggregated Over PAR",
        units     = "m-1",
    ),
    "phycocyanin":
    ESACCILakesVariable(
        var_id    = "phycocyanin",
        long_name = "Concentration of Phycocyanin Calculated From MDN Algorithm by O'Shea et al. 2021",
        units     = "mg.m-3",
    ),
    "lake_surface_water_temperature":
    ESACCILakesVariable(
        var_id    = "lake_surface_water_temperature",
        long_name = "Lake Surface Skin Temperature",
        units     = "°C",
    ),
    "lake_surface_water_extent":
    ESACCILakesVariable(
        var_id    = "lake_surface_water_extent",
        long_name = "Lake Water Extent",
        units     = "km2",
    ),
}
