"""
Filename:   wfsel.sources.esacci_lakes.computers.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Related Third-party Imports
import numpy    as np
import pandas   as pd

# Local Application/Library Specific Imports
from wfsel.sources.esacci_lakes.models import Season


def compute_observations_mean(
    observations: list[pd.Series[float]],
) -> pd.Series[float]:
    """
    Compute an element-wise mean across a list of observations series.

    Parameters
    ----------
    observations : list[pd.Series[float]]
        The list of observations series

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


def compute_observations_std(
    observations: list[pd.Series[float]],
) -> pd.Series[float]:
    """
    Compute an element-wise standard deviation across a list of
    observations series.

    Parameters
    ----------
    observations : list[pd.Series[float]]
        The list of observations series

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


def compute_pre_season_mean(
    season: Season,
    start:  int,
    stop:   int,
) -> float | None:
    """
    Compute a pre-season mean.

    Parameters
    ----------
    season : Season
        The season
    start : int
        The start of the slice, inclusive. Computed as an offset from
        season.first
    stop : int
        The stop of the slice, inclusive. Computed as an offset from
        season.first

    Returns
    -------
    float | None
        A pre-season mean, or None if mean was NaN
    """
    start   = season.first - start
    stop    = season.first - stop

    pre_season_mean = (
                        season
                        .observations_ser
                        .loc[start:stop]
                        .mean()
                    )

    if np.isnan(pre_season_mean):
        return None

    return pre_season_mean


def compute_pre_season_std(
    season: Season,
    start:  int,
    stop:   int,
) -> float | None:
    """
    Compute a pre-season standard deviation.

    Parameters
    ----------
    season : Season
        The season
    start : int
        The start of the slice, inclusive. Computed as an offset from
        season.first
    stop : int
        The stop of the slice, inclusive. Computed as an offset from
        season.first

    Returns
    -------
    float | None
        A pre-season standard deviation, or None if standard deviation
        was NaN
    """
    start   = season.first - start
    stop    = season.first - stop

    pre_season_std  = (
                        season
                        .observations_ser
                        .loc[start:stop]
                        .std()
                    )

    if np.isnan(pre_season_std):
        return None

    return pre_season_std
