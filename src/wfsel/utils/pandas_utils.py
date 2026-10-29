"""
Filename:   wfsel.utils.pandas_utils.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Related Third-party Imports
import pandas as pd


def compute_quantiles(
    ser:    pd.Series[float],
    levels: list[float],
) -> list[float]:
    """
    Compute the quantiles of a series.

    Parameters
    ----------
    ser : pd.Series
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
