r"""
utils.py

Description:
   Provides definitions for math-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
import re

# Related Third-party Imports
import pandas as pd


def drop_column_from_df(
    df:     pd.DataFrame,
    column: str
) -> pd.DataFrame:
    """
    Returns `df` with `column` dropped.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    column : :class:`str`
        The column to drop

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return df.drop(columns=[column])


def filter_df_by_column_bounds(
    df:     pd.DataFrame,
    column: str,
    *,
    lower:  float | None = None,
    upper:  float | None = None
) -> pd.DataFrame:
    """
    Filters `df` to rows whose `column` is within [`lower`, `upper`].

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    column : :class:`str`
        The column to filter on

    lower : float | None
        Inclusive lower bound. If `None`, no lower bound is applied.
        default=None

    upper : float | None
        Inclusive upper bound. If `None`, no upper bound is applied.
        default=None

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Notes
    -----
    Internal indexing call assumes `column` is an existing column in
    `df`.
    """
    if lower is not None:
        df = df[df[column] >= lower]

    if upper is not None:
        df = df[df[column] <= upper]

    return df


def intersect_dfs_by_columns(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns `left_df` and `right_df` restricted to their common
    columns.

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left :class:`pandas.DataFrame`

    right_df : :class:`pandas.DataFrame`
        The right :class:`pandas.DataFrame`

    Returns
    -------
    A tuple of (`left_df`, `right_df`), each restricted to columns
    present in both.
    """
    columns = left_df.columns.intersection(right_df.columns)

    return left_df[columns], right_df[columns]


def intersect_dfs_by_rows(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns `left_df` and `right_df` restricted to their common rows.

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left :class:`pandas.DataFrame`

    right_df : :class:`pandas.DataFrame`
        The right :class:`pandas.DataFrame`

    Returns
    -------
    A tuple of (`left_df`, `right_df`), each restricted to rows (by
    index) present in both.
    """
    rows = left_df.index.intersection(right_df.index)

    return left_df.loc[rows], right_df.loc[rows]


def intersect_dfs_by_cells(
    left_df:  pd.DataFrame,
    right_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns `left_df` and `right_df` with each cell blanked (set to
    `NaN`) wherever the corresponding cell is `NaN` in either.

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left :class:`pandas.DataFrame`

    right_df : :class:`pandas.DataFrame`
        The right :class:`pandas.DataFrame`

    Returns
    -------
    A tuple of (`left_df`, `right_df`), cell-aligned so both share the
    same pattern of missing values.

    Raises
    ------
    ValueError
        If `left_df` and `right_df` do not share identical shape,
        columns, or index.

    Notes
    -----
    Assumes `left_df` and `right_df` have identical shape, columns, and
    index.
    """
    if left_df.shape != right_df.shape:
        raise ValueError("expected `left_df` and `right_df` to have identical shape")

    if not left_df.columns.equals(right_df.columns):
        raise ValueError("expected `left_df` and `right_df` to have identical columns")

    if not left_df.index.equals(right_df.index):
        raise ValueError("expected `left_df` and `right_df` to have identical index")

    combined_mask = left_df.notna() & right_df.notna()

    return left_df.where(combined_mask), right_df.where(combined_mask)


def normalise_df(
    df:     pd.DataFrame,
    column: str
) -> pd.DataFrame:
    """
    Returns `df` with every column subtracted by `column`.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    column : :class:`str`
        The column to subtract from every column, row-wise

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Notes
    -----
    Internal `pandas.DataFrame.sub` call assumes `column` is an
    existing column in `df`.
    """
    return df.sub(
        df[column],
        axis=0
    )


def sort_df_columns_alphabetically(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns `df` with its columns sorted alphabetically.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return df.sort_index(axis='columns')


def sort_df_columns_numerically(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns `df` with its columns sorted numerically, by the number(s)
    embedded in each column name.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Notes
    -----
    Column names are sorted by the numeric value(s) extracted from
    them (e.g. "w_-3" sorts before "w_2"). Columns with no embedded
    number sort first.
    """
    def key(
        column: str
    ) -> tuple[float, ...]:
        matches = re.findall(
            r'-?\d+',
            column
        )

        if matches:
            return tuple(map(float, matches))
        else:
            return (float('-inf'),)

    columns = sorted(
        df.columns,
        key=key
    )

    return df.reindex(columns=columns)


def get_ser_from_df(
    df:     pd.DataFrame,
    column: str
) -> pd.Series:
    """
    Get a `df`'s `column` as a :class:`pandas.Series`.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    column : :class:`str`
        The column to return

    Returns
    -------
    A :class:`pandas.Series`.
    """
    return df[column]


def get_quantiles_from_ser(
    ser:       pd.Series,
    quantiles: list[float]
) -> list[float]:
    """
    Get a `ser`'s values at each of `quantiles`.

    Parameters
    ----------
    ser : :class:`pandas.Series`
        The :class:`pandas.Series`

    quantiles : list[float]
        The quantiles to compute, e.g. `[0.25, 0.5, 0.75]` for Q1, Q2,
        and Q3

    Returns
    -------
    A list of computed quantile values, in the same order as
    `quantiles`.
    """
    return [
        ser.quantile(quantile)
        for quantile 
        in quantiles
    ]


def ser_is_strictly_positive(
    ser: pd.Series
) -> bool:
    """
    Checks if every value in `ser` is greater than 0.

    Parameters
    ----------
    ser : :class:`pandas.Series`
        The :class:`pandas.Series`

    Returns
    -------
    `True` if `ser.dropna().min() > 0`. `False` otherwise.

    Raises
    ------
    ValueError
        If `ser` has no non-NaN values.

    Notes
    -----
    Assumes `ser` has at least one non-NaN value.
    """
    ser = ser.dropna()

    if ser.empty:
        raise ValueError("expected `ser` to have at least one non-NaN value")

    return ser.min() > 0
