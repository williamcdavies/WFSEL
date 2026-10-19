"""
wfsel.utils.geopandas_utils.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import geopandas as gpd


def filter_gdf_rows_by_values(
    gdf:     gpd.GeoDataFrame,
    colname: str,
    values:  list[str],
) -> gpd.GeoDataFrame:
    """
    Filter a GeoDataFrame by values.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        The GeoDataFrame
    colname : str
        The column name
    values : list[str]
        The values

    Returns
    -------
    gpd.GeoDataFrame
    """
    gdf = gdf[gdf[colname].isin(values)]

    return gdf
