r"""
utils.py

Description:
   Provides definitions for esacci_lakes-utility variables.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import psycopg.sql

# Local Application/Library Specific Imports
from lib.esacci_lakes.objects import ESACCILakesVariable

# Average depth variables
# ==================================================================================================
AVERAGE_DEPTH_LOWER_BOUND = 10
AVERAGE_DEPTH_UPPER_BOUND = 50
# ==================================================================================================

# Count of distinct start days variables
# ==================================================================================================
COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND = 7
COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND = 42
COUNT_OF_DISTINCT_START_DAYS_QUERY       = psycopg.sql.SQL("""
WITH xref AS (
    SELECT l.geom
    FROM esacci_lakes AS l
    WHERE l.id = %(id)s
)

SELECT DISTINCT ON (s.start_day) s.start_day AS "day"
FROM {table} AS s
JOIN xref AS x
    ON ST_INTERSECTS(s.geom, x.geom)
WHERE s.density > 1
ORDER BY s.start_day
""")
# ==================================================================================================

# ESA CCI Lakes variables
# ==================================================================================================
ESACCI_LAKES_VARIABLES = {
    "chla": ESACCILakesVariable(
        "chla",
        "Concentration of Chlorophyll-a",
        "mg.m-3",
    ),
    "tsm": ESACCILakesVariable(
        "tsm",
        "Concentration of Total Suspended Matter",
        "g.m-3",
    ),
    "acdom440": ESACCILakesVariable(
        "acdom440",
        "Absorption Coefficient of Coloured Dissolved Organic Matter at 440 nm",
        "m-1",
    ),
    "Kd490": ESACCILakesVariable(
        "Kd490",
        "Vertical Diffuse Downwelling Attenuation Coefficient at 490 nm",
        "m-1",
    ),
    "KdPAR": ESACCILakesVariable(
        "KdPAR",
        "Vertical Diffuse Downwelling Attenuation Coefficient Aggregated Over PAR",
        "m-1",
    ),
    "phycocyanin": ESACCILakesVariable(
        "phycocyanin",
        "Concentration of Phycocyanin Calculated From MDN Algorithm by O'Shea et al. 2021",
        "mg.m-3",
    ),
    "lake_surface_water_temperature": ESACCILakesVariable(
        "lake_surface_water_temperature",
        "Lake Surface Skin Temperature",
        "˚C",
    ),
    "lake_surface_water_extent": ESACCILakesVariable(
        "lake_surface_water_extent",
        "Lake Water Extent",
        "km2",
    ),
}
# ==================================================================================================
