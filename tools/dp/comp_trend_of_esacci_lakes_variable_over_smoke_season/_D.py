r"""
D.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

# Related Third-party Imports
import numpy  as np
import pandas as pd
import psycopg

# Local Application/Library Specific Imports
from _shared                     import (
    arguments_are_valid,
    build_parser,
    get_esacci_lakes_interest_ranges_df,
    get_esacci_lakes_smoke_season_ranges_df,
    get_esacci_lakes_years_df
)
from lib.esacci_lakes.utils.proc import read_esacci_lakes_counts_of_distinct_start_days_csv
from lib.esacci_lakes.vars       import (
    COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND,
    COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)


# Years functions
# ==================================================================================================
def get_esacci_lakes_high_years_df(
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of each lake's years whose
    count of distinct start days is at least
    `COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND`.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    Returns
    -------
    A :class:`pandas.DataFrame` with columns "esacci_lakes_id" and
    "year", and one row per qualifying (lake, year) pair.
    """
    return get_esacci_lakes_years_df(
        esacci_lakes_counts_of_distinct_start_days_df,
        lower_bound = COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
    )


def get_esacci_lakes_low_years_df(
    esacci_lakes_counts_of_distinct_start_days_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of each lake's years whose
    count of distinct start days is at most
    `COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND`.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes counts of distinct start days

    Returns
    -------
    A :class:`pandas.DataFrame` with columns "esacci_lakes_id" and
    "year", and one row per qualifying (lake, year) pair.
    """
    return get_esacci_lakes_years_df(
        esacci_lakes_counts_of_distinct_start_days_df,
        upper_bound = COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND
    )


# ==================================================================================================


# Smoke season range functions
# ==================================================================================================
def get_esacci_lakes_median_smoke_season_ranges_df(
    esacci_lakes_smoke_season_ranges_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of
    `esacci_lakes_smoke_season_ranges_df` aggregated by the medians of
    the first and last days of the smoke season.

    Parameters
    ----------
    esacci_lakes_smoke_season_ranges_df : :class:`pandas.DataFrame`
        The smoke season ranges, with columns "esacci_lakes_id", "year",
        "first_day_of_smoke_season", and "last_day_of_smoke_season"

    Returns
    -------
    A :class:`pandas.DataFrame` with columns "esacci_lakes_id", "year",
    "first_day_of_interest", and "last_day_of_interest".
    """
    return pd.DataFrame()


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    counts_of_distinct_start_days_df = read_esacci_lakes_counts_of_distinct_start_days_csv(args.esacci_lakes_counts_of_distinct_start_days_csv_path)

    high_years_df = get_esacci_lakes_high_years_df(counts_of_distinct_start_days_df)
    low_years_df  = get_esacci_lakes_low_years_df(counts_of_distinct_start_days_df)

    with psycopg.connect("dbname=spatial") as connection:
        smoke_season_ranges_df = get_esacci_lakes_smoke_season_ranges_df(
            high_years_df,
            connection
        )

    smoke_season_ranges_df = get_esacci_lakes_median_smoke_season_ranges_df(smoke_season_ranges_df)

    interest_ranges_df = get_esacci_lakes_interest_ranges_df(smoke_season_ranges_df)

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())