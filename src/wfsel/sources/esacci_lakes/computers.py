"""
wfsel.sources.esacci_lakes.computers.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd


def mean_observations(
    observations: list[pd.Series[float]],
) -> pd.Series[float]:
    """
    Compute an element-wise mean across a list of observation series.

    Parameters
    ----------
    observations : list[pd.Series[float]]
        The list of observation series

    Returns
    -------
    pd.Series[float]
        An observation series
    """
    mean    = (
                pd.DataFrame(observations)
                .mean(axis = 0)
                .astype(float)
            )

    return mean


def std_observations(
    observations: list[pd.Series[float]],
) -> pd.Series[float]:
    """
    Compute an element-wise standard deviation across a list of
    observation series.

    Parameters
    ----------
    observations : list[pd.Series[float]]
        The list of observation series

    Returns
    -------
    pd.Series[float]
        An observation series
    """
    std = (
            pd.DataFrame(observations)
            .std(axis = 0)
            .astype(float)
        )

    return std
