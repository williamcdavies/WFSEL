"""
Filename:   wfsel.math.computers.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd


def compute_quantiles(
    ser:    pd.Series[float],
    levels: list[float],
) -> list[float]:
    """
    Compute a list of quantiles.

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
