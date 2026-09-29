r"""
utils.py

Description:
    Provides definitions for stat-utility functions.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd

from scipy.stats import ttest_rel


def get_ttest_result(
    a:           pd.Series,
    b:           pd.Series,
    *,
    alternative: str
):
    """
    Returns the paired t-test result of `a` against `b`.

    Parameters
    ----------
    a : :class:`pandas.Series`
        The series

    b : :class:`pandas.Series`
        The series

    alternative : :class:`str`
        The alternative hypothesis

    Returns
    -------
    A :class:`scipy.stats.TtestResult`.

    Raises
    ------
    ValueError
        If `a` and `b` are not of equal length, or not of equal index.
    """
    if len(a) != len(b):
        raise ValueError("expected `a` and `b` to be of equal length")

    if not a.index.equals(b.index):
        raise ValueError("expected `a` and `b` to be of equal index")

    return ttest_rel(
        a,
        b,
        alternative = alternative
    )
