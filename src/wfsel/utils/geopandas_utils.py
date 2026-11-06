"""
Filename:   wfsel.utils.geopandas_utils.py
Author:     William Chuter-Davies
Modified:   06/11/26
"""

# Related Third-party Imports
import geopandas as gpd


def filter_gdf_by_values(
    gdf:            gpd.GeoDataFrame,
    column_name:    str,
    values:         list[str],
) -> gpd.GeoDataFrame:
    """
    Filter a geodataframe by a list of values.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        The geodataframe
    column_name : str
        The column name
    values : list[str]
        The list of values

    Returns
    -------
    gpd.GeoDataFrame
        A geodataframe
    """
    gdf = gdf[gdf[column_name].isin(values)]

    return gdf
