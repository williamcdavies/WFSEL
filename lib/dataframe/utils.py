r"""
utils.py

Description:
    Provides definitions for dataframe-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
import re

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.phys.vars import FREEZING_POINT_OF_WATER_K


# DataFrame functions
# ==================================================================================================
def convert_df_from_kelvin_to_celsius(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Converts `df`'s units from Kelvin to Celsius.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return df - FREEZING_POINT_OF_WATER_K


def drop_column_from_df(
    df:     pd.DataFrame,
    column: str
) -> pd.DataFrame:
    """
    Returns `df` with `column` dropped.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    column : :class:`str`
        The column

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return df.drop(columns = [column])


def filter_df_by_column_bounds(
    df:     pd.DataFrame,
    column: str,
    *,
    lower:           float | None = None,
    upper:           float | None = None,
    lower_inclusive: bool = True,
    upper_inclusive: bool = True
) -> pd.DataFrame:
    """
    Filters `df` to rows whose `column` value(s) lie between `lower` and
    `upper`.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    column : :class:`str`
        The column

    lower : :class:`float` | `None`
        Lower bound, inclusive if `lower_inclusive`. If `None`, no lower bound
        is applied. default=None

    upper : :class:`float` | `None`
        Upper bound, inclusive if `upper_inclusive`. If `None`, no upper bound
        is applied. default=None

    lower_inclusive : :class:`bool`
        If `True`, rows where `column` equals `lower` pass. default=True

    upper_inclusive : :class:`bool`
        If `True`, rows where `column` equals `upper` pass. default=True

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    if lower is not None:
        if lower_inclusive:
            df = df[df[column] >= lower]
        else:
            df = df[df[column] > lower]

    if upper is not None:
        if upper_inclusive:
            df = df[df[column] <= upper]
        else:
            df = df[df[column] < upper]

    return df


def intersect_dfs_by_cells(
    left_df:  pd.DataFrame,
    right_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns `left_df` and `right_df` with (NaN, not NaN) and (not NaN, NaN)
    pairs set to (NaN, NaN).

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left dataframe

    right_df : :class:`pandas.DataFrame`
        The right dataframe

    Returns
    -------
    A tuple of (`left_df`, `right_df`).

    Raises
    ------
    ValueError
        If `left_df` and `right_df` are not of similar shape, columns, and
        index.
    """
    if left_df.shape != right_df.shape:
        raise ValueError("expected `left_df` and `right_df` to be of similar shape")

    if not left_df.columns.equals(right_df.columns):
        raise ValueError("expected `left_df` and `right_df` to be of similar columns")

    if not left_df.index.equals(right_df.index):
        raise ValueError("expected `left_df` and `right_df` to be of similar index")

    mask = left_df.notna() & right_df.notna()

    return (
        left_df.where(mask),
        right_df.where(mask)
    )


def intersect_dfs_by_columns(
    left_df:  pd.DataFrame,
    right_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns `left_df` and `right_df` restricted to their shared columns.

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left dataframe

    right_df : :class:`pandas.DataFrame`
        The right dataframe

    Returns
    -------
    A tuple of (`left_df`, `right_df`).
    """
    columns = left_df.columns.intersection(right_df.columns)

    return (
        left_df[columns],
        right_df[columns]
    )


def intersect_dfs_by_rows(
    left_df:  pd.DataFrame,
    right_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns `left_df` and `right_df` restricted to their shared rows.

    Parameters
    ----------
    left_df : :class:`pandas.DataFrame`
        The left dataframe

    right_df : :class:`pandas.DataFrame`
        The right dataframe

    Returns
    -------
    A tuple of (`left_df`, `right_df`).
    """
    rows = left_df.index.intersection(right_df.index)

    return (
        left_df.loc[rows],
        right_df.loc[rows]
    )


def sort_df_columns_alphabetically(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns `df` with columns sorted alphabetically.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return df.sort_index(axis = "columns")


def sort_df_columns_numerically(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns `df` with columns sorted numerically.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    def _key(
        column: str
    ) -> tuple[float, ...]:
        matches = re.findall(
            r"-?\d+",
            column
        )

        if matches:
            return tuple(map(
                float,
                matches
            ))

        return (float("-inf"),)

    columns = sorted(
        df.columns,
        key = _key
    )

    return df.reindex(columns = columns)


def subtract_columns_mean_from_df(
    df:      pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Returns `df` with the row-wise mean of `columns` subtracted from every
    column.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    columns : list[:class:`str`]
        The columns

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return df.sub(
        df[columns].mean(axis = 1),
        axis = 0
    )


# ==================================================================================================


# Series functions
# ==================================================================================================
def get_quantiles_from_ser(
    ser:       pd.Series,
    quantiles: list[float]
) -> list[float]:
    """
    Returns `ser`'s values at each of `quantiles`.

    Parameters
    ----------
    ser : :class:`pandas.Series`
        The series

    quantiles : list[:class:`float`]
        The quantiles

    Returns
    -------
    A list of :class:`float`.
    """
    return [
        float(ser.quantile(quantile))
        for quantile
        in quantiles
    ]


def get_ser_from_df(
    df:     pd.DataFrame,
    column: str
) -> pd.Series:
    """
    Returns `df`'s `column` as a :class:`pandas.Series`.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The dataframe

    column : :class:`str`
        The column

    Returns
    -------
    A :class:`pandas.Series`.
    """
    return df[column]


def ser_is_strictly_positive(
    ser: pd.Series
) -> bool:
    """
    Returns `True` if every non-NaN value in `ser` is greater than 0.

    Parameters
    ----------
    ser : :class:`pandas.Series`
        The series

    Returns
    -------
    `True` if every non-NaN value in `ser` is greater than 0. `False` otherwise.

    Raises
    ------
    ValueError
        If `ser` has no non-NaN values.
    """
    ser = ser.dropna()

    if ser.empty:
        raise ValueError("expected `ser` to have at least one non-NaN value")

    return ser.min() > 0


# ==================================================================================================
