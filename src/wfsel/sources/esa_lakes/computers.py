"""
Filename:   wfsel.sources.esa_lakes.computers.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import numpy    as np
import pandas   as pd

# Local Application/Library Specific Imports
from wfsel.literals                 import Statistic
from wfsel.sources.esa_lakes.models import Season


def _compute_observations_ser_list_statistic(
    observations_ser_list:  list[pd.Series[float]],
    statistic:              Statistic,
) -> pd.Series[float]:
    """
    Compute an element-wise statistic across a list of observations series.

    Parameters
    ----------
    observations_ser_list : list[pd.Series[float]]
        The list of observations series
    statistic : Statistic
        The statistic

    Returns
    -------
    pd.Series[float]
        An observations series
    """
    df = pd.DataFrame(observations_ser_list)

    match statistic:
        case "mean":
            result  = df.mean(axis = 0).astype(float)
        case "std":
            result  = df.std(axis = 0).astype(float)

    return result


def compute_observations_ser_list_mean(
    observations_ser_list: list[pd.Series[float]],
) -> pd.Series[float]:
    """
    Compute an element-wise mean across a list of observations series.

    Parameters
    ----------
    observations_ser_list : list[pd.Series[float]]
        The list of observations series

    Returns
    -------
    pd.Series[float]
        An observations series
    """
    mean    = _compute_observations_ser_list_statistic(
                observations_ser_list,
                "mean",
            )

    return mean


def compute_observations_ser_list_std(
    observations_ser_list: list[pd.Series[float]],
) -> pd.Series[float]:
    """
    Compute an element-wise standard deviation across a list of
    observations series.

    Parameters
    ----------
    observations_ser_list : list[pd.Series[float]]
        The list of observations series

    Returns
    -------
    pd.Series[float]
        An observations series
    """
    std = _compute_observations_ser_list_statistic(
            observations_ser_list,
            "std",
        )

    return std


def _compute_pre_season_statistic(
    season:     Season,
    start:      int,
    stop:       int,
    statistic:  Statistic,
) -> float | None:
    """
    Compute a pre-season statistic.

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
    statistic : Statistic
        The statistic

    Returns
    -------
    float | None
        A pre-season statistic, or None if the statistic was NaN
    """
    start_index = season.first - start
    stop_index  = season.first - stop

    pre_season_slice    = (
                            season
                            .observations_ser
                            .loc[start_index:stop_index]
                        )

    match statistic:
        case "mean":
            pre_season_statistic = pre_season_slice.mean()
        case "std":
            pre_season_statistic = pre_season_slice.std()

    if np.isnan(pre_season_statistic):
        return None

    return pre_season_statistic


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
        A pre-season mean, or None if the mean was NaN
    """
    mean    = _compute_pre_season_statistic(
                season,
                start,
                stop,
                "mean",
            )

    return mean


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
        A pre-season standard deviation, or None if the standard
        deviation was NaN
    """
    std = _compute_pre_season_statistic(
            season,
            start,
            stop,
            "std",
        )

    return std
