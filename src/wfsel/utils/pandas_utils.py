"""
wfsel.utils.pandas_utils.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd


def compute_quantiles(
    ser:    pd.Series,
    levels: list[float],
) -> list[float]:
    """
    Compute the quantiles of a Series.

    Parameters
    ----------
    ser : pd.Series
        The Series
    levels : list[float]
        The levels

    Returns
    -------
    list[float]
    """
    quantiles = [
        float(ser.quantile(level))
        for level
        in levels
    ]

    return quantiles
