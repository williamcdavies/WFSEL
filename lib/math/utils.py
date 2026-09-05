r"""
utils.py

Description:
   Provides definitions for math-utility functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import pandas     as pd


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
    """
    return ser.dropna().min() > 0
