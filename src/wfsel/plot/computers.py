"""
Filename:   wfsel.plot.computers.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd

from scipy.stats import gaussian_kde


def compute_kde(
    ser: pd.Series[float],
) -> tuple[pd.Series[float], pd.Series[float]]:
    """
    Compute a KDE.

    Parameters
    ----------
    ser : pd.Series[float]
        The series

    Returns
    -------
    tuple[pd.Series[float], pd.Series[float]]
        A tuple of x- and y-values
    """
    ser_nonan   = ser.dropna()
    kde         = gaussian_kde(ser_nonan)
    x_values    = ser_nonan.sort_values()
    y_values    = pd.Series(kde(x_values))

    return x_values, y_values
