r"""
utils.py

Description:
   Provides definitions for db-utility functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import geopandas  as gpd
import pandas     as pd
import sqlalchemy


def get_df_from_postgis(
    query:      str,
    connection: sqlalchemy.Connection
) -> pd.DataFrame:
    """
    Get a :class:`pandas.DataFrame` from a query and a :class:`sqlalchemy.Connection`.

    Parameters
    ----------
    query : :class:`str`
        The query

    connection : :class:`sqlalchemy.Connection`
        The connection

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_sql(query, connection)


def get_gdf_from_postgis(
    query:      str,
    connection: sqlalchemy.Connection
) -> gpd.GeoDataFrame:
    """
    Get a :class:`geopandas.GeoDataFrame` from a query and a
    :class:`sqlalchemy.Connection`.

    Parameters
    ----------
    query : :class:`str`
        The query

    connection : :class:`sqlalchemy.Connection`
        The connection

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.

    Notes
    -----
    Internal `geopandas.read_postgis` call assumes geom_col="geom".
    """
    return gpd.read_postgis(
        query,
        connection
    )
