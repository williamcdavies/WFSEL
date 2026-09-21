r"""
fataframe.py

Description:
    Provides definitions for esacci_lakes-utility dataframe functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.esacci_lakes.vars import HYLAK_FIELDS


def drop_hylak_field_columns_from_df(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns `df` with all `HYLAK_FIELDS` columns dropped.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return df.drop(
        columns = list(HYLAK_FIELDS),
        errors  = "ignore"
    )


def merge_dfs_on_esacci_lakes_id(
    left_df:  pd.DataFrame,
    right_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merges `left_df` with `right_df` on the `esacci_lakes_id` index.

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left dataframe

    right_df : :class:`pandas.DataFrame`
        The right dataframe

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Raises
    ------
    ValueError
        If `left_df.index.name` or `right_df.index.name` is not
        "esacci_lakes_id".
    """
    if (
        left_df.index.name != "esacci_lakes_id"
        or right_df.index.name != "esacci_lakes_id"
    ):
        raise ValueError("expected `esacci_lakes_id` as the index name of both `left_df` and `right_df`")

    return pd.merge(
        left        = left_df,
        right       = right_df,
        left_index  = True,
        right_index = True,
        validate    = "one_to_one"
    )
    