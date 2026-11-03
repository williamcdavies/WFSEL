"""
Filename:   wfsel.math.computers.py
Author:     William Chuter-Davies
Modified:   03/11/26
"""

# Related Third-party Imports
import pandas as pd

from scipy.stats import gaussian_kde


def compute_kde(
    ser: pd.Series[float],
) -> gaussian_kde:
    """
    Compute a KDE from a series.

    Parameters
    ----------
    ser : pd.Series[float]
        The series

    Returns
    -------
    gaussian_kde
        A KDE
    """
    return gaussian_kde(ser)
