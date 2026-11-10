"""
Filename:   wfsel.utils.geopandas_utils.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from typing import Any

# Related Third-party Imports
import geopandas as gpd


def filter_gdf_by_values(
    gdf:            gpd.GeoDataFrame,
    column_name:    str,
    values:         list[Any],
) -> gpd.GeoDataFrame:
    """
    Filter a geodataframe by a list of values.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        The geodataframe
    column_name : str
        The column name
    values : list[Any]
        The list of values

    Returns
    -------
    gpd.GeoDataFrame
        A geodataframe
    """
    filtered_gdf = gdf[gdf[column_name].isin(values)]

    return filtered_gdf
