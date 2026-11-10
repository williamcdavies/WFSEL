"""
Filename:   wfsel.utils.pandas_utils.py
Author:     William Chuter-Davies
"""

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


def compute_quantiles(
    ser:    pd.Series[float],
    levels: list[float],
) -> list[float]:
    """
    Compute a list of quantiles from a series.

    Parameters
    ----------
    ser : pd.Series[float]
        The series
    levels : list[float]
        The list of levels

    Returns
    -------
    list[float]
        A list of quantiles
    """
    quantiles   = [
                    float(ser.quantile(level))
                    for level
                    in levels
                ]

    return quantiles
