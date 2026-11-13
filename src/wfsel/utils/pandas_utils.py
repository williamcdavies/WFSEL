"""
Filename:   wfsel.utils.pandas_utils.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from typing import Any

# Related Third-party Imports
import pandas as pd


def build_mask_from_index_ser(
    index_ser:  pd.Series[int],
    start:      int,
    stop:       int,
) -> pd.Series[int]:
    """
    Build a mask from a series of indices.

    Parameters
    ----------
    index_ser : pd.Series[int]
        The index series
    start : int
        The start of the range index, inclusive
    stop : int
        The stop of the range index, exclusive

    Returns
    -------
    pd.Series[int]
        A mask series
    """
    mask    = pd.Series(
                0,
                pd.RangeIndex(
                    start,
                    stop,
                ),
            )

    mask.loc[index_ser] = 1

    return mask


def filter_df_by_index(
    df:             pd.DataFrame,
    index_name:     str,
    index_values:   list[Any],
) -> pd.DataFrame:
    """
    Filter a dataframe by a list of index values.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe
    index_name : str
        The index name
    index_values : list[Any]
        The list of index values

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    filtered_df = df[df.index.get_level_values(index_name).isin(index_values)]

    return filtered_df


def filter_df_by_values(
    df:             pd.DataFrame,
    column_name:    str,
    column_values:  list[Any],
) -> pd.DataFrame:
    """
    Filter a dataframe by a list of column values.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe
    column_name : str
        The column name
    values : list[Any]
        The list of column values

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    filtered_df = df[df[column_name].isin(column_values)]

    return filtered_df
