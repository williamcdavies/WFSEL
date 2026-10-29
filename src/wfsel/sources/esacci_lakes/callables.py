"""
Filename:   wfsel.sources.esacci_lakes.callables.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Standard Library Imports
from collections.abc import Callable

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.sources.esacci_lakes.models import Season


def apply_season_function(
    observations_ser:   pd.Series[float],
    season_fn:          Callable[[], tuple[int, int] | None],
) -> Season | None:
    """
    Construct a season with a season function.

    Parameters
    ----------
    observations_ser : pd.Series[float]
        The observations series
    season_fn : Callable[[], tuple[int, int]  |  None]
        The season function

    Returns
    -------
    Season | None
        A season, or None if the season function fails
    """
    if (r := season_fn()) is None:
        return None

    (
        first,
        last,
    ) = r

    season  = Season(
                observations_ser    = observations_ser,
                first               = first,
                last                = last,
            )

    return season


def season_function_sliding_window(
    distinct_labels_ser: pd.Series[int],
    *,
    width:      int,
    trigger:    int,
    edge:       str,
) -> tuple[int, int] | None:
    """
    Season function: sliding window.

    Parameters
    ----------
    distinct_labels_ser : pd.Series[int]
        The distinct labels series
    width : int
        The width
    trigger : int
        The trigger
    edge : str
        The edge

    Returns
    -------
    tuple[int, int] | None
        A (first, last) pair, or None if no valid pair was found
    """
    def _compute_first(
    ) -> int | None:
        for i in range(
            trigger - 1,
            len(distinct_labels_ser),
        ):
            left    = distinct_labels_ser.iloc[i - (trigger - 1)]
            right   = distinct_labels_ser.iloc[i]

            if right - left < width:
                match edge:
                    case "left":
                        return left
                    case "right":
                        return right
                    case _:
                        message = f'expected edge to be in ["left", "right"]: got {edge}'

                        raise ValueError(message)

        return None


    def _compute_last(
    ) -> int | None:
        for i in reversed(range(
            trigger - 1,
            len(distinct_labels_ser),
        )):
            left    = distinct_labels_ser.iloc[i - (trigger - 1)]
            right   = distinct_labels_ser.iloc[i]

            if right - left < width:
                match edge:
                    case "left":
                        return left
                    case "right":
                        return right
                    case _:
                        message = f'expected edge to be in ["left", "right"]: got {edge}'

                        raise ValueError(message)

        return None


    first   = _compute_first()
    last    = _compute_last()

    if (
            first is None
        or  last is None
    ):
        return None

    return (
        first,
        last,
    )


def season_function_interest(
    season: Season,
    *,
    lookback:   int,
    lookahead:  int,
) -> tuple[int, int] | None:
    """
    Season function: interest.

    Parameters
    ----------
    season : Season
        The season
    lookback : int
        The lookback
    lookahead : int
        The lookahead

    Returns
    -------
    tuple[int, int] | None
        A (first, last) pair, or None if no valid pair was found
    """
    first   = season.first - lookback
    last    = season.first + lookahead

    if (
            first < season.observations_ser.index[0]
        or  last > season.observations_ser.index[-1]
    ):
        return None

    return (
        first,
        last,
    )
