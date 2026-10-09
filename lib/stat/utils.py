r"""
utils.py

Description:
    Provides definitions for stat-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from typing import Literal

# Related Third-party Imports
import pandas as pd

from scipy.stats                 import ttest_rel
from scipy.stats._result_classes import TtestResult


# Test functions
# ==================================================================================================
def get_ttest_result(
    sample_a:    pd.Series,
    sample_b:    pd.Series,
    alternative: Literal["two-sided", "less", "greater"]
) -> TtestResult:
    """
    Returns the paired t-test result of `sample_a` against `sample_b`.

    Parameters
    ----------
    sample_a : :class:`pandas.Series`
        The first sample

    sample_b : :class:`pandas.Series`
        The second sample

    alternative : :class:`str`
        The alternative hypothesis

    Returns
    -------
    A :class:`scipy.stats._result_classes.TtestResult`.

    Raises
    ------
    ValueError
        If `sample_a` and `sample_b` are not of equal index.
    """
    if not sample_a.index.equals(sample_b.index):
        raise ValueError("expected `sample_a` and `sample_b` to be of equal index")

    return ttest_rel(
        sample_a,
        sample_b,
        alternative = alternative
    )


# ==================================================================================================
