r"""
math.py

Description:
   Provides definitions for esacci_lakes-utility math functions.

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
        The :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Notes
    -----
    Columns in `HYLAK_FIELDS` that are not present in `df` are
    silently ignored.
    """
    return df.drop(
        columns=list(HYLAK_FIELDS),
        errors="ignore"
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
        The left :class:`pandas.DataFrame`

    right_df : :class:`pandas.DataFrame`
        The right :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Raises
    ------
    ValueError
        If `left_df.index.name` or `right_df.index.name` is not
        "esacci_lakes_id".

    Notes
    -----
    Internal `pandas.merge` call assumes "esacci_lakes_id" is the index
    of both `left_df` and `right_df`. Merge is validated as one-to-one.
    """
    if (   
        left_df.index.name != "esacci_lakes_id" 
        or right_df.index.name != "esacci_lakes_id"
    ):
        raise ValueError("expected \"esacci_lakes_id\" as the index name of both `left_df` and `right_df`")

    return pd.merge(
        left=left_df,
        right=right_df,
        left_index=True,
        right_index=True,
        validate="one_to_one"
    )
    