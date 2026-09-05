r"""
tabular.py

Description:
   Provides definitions for esacci_lakes-utility math functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd


def merge_dfs_on_esacci_lakes_id(
    left_df:  pd.DataFrame,
    right_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merges a `left_df` with `right_df` on `esacci_lakes_id`.

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left :class:`pandas.DataFrame`

    right_df : :class:`pandas.DataFrame`
        The right :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Notes
    -----
    Internal `pandas.merge` call assumes "esacci_lakes_id" is an
    existing column in both `left_df` and `right_df`. Merge is validated
    as one-to-one.
    """
    return pd.merge(
        left=left_df,
        right=right_df,
        on="esacci_lakes_id",
        validate="one_to_one"
    )


def merge_dfs_on_hylak_id(
    left_df:  pd.DataFrame,
    right_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merges a `left_df` with `right_df` on `hylak_id`.

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left :class:`pandas.DataFrame`

    right_df : :class:`pandas.DataFrame`
        The right :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Notes
    -----
    Internal `pandas.merge` call assumes "hylak_id" is an existing
    column in both `left_df` and `right_df`. Merge is validated as
    one-to-one.
    """
    return pd.merge(
        left=left_df,
        right=right_df,
        on="hylak_id",
        validate="one_to_one"
    )
