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
    Returns a :class:`pandas.DataFrame` from `query` and `connection`.

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
    Returns a :class:`geopandas.GeoDataFrame` from `query` and
    `connection`.

    Parameters
    ----------
    query : :class:`str`
        The query

    connection : :class:`sqlalchemy.Connection`
        The connection

    Returns
    -------
    A :class:`geopandas.GeoDataFrame`.
    """
    return gpd.read_postgis(
        query,
        connection
    )
