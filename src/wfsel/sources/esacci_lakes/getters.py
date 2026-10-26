"""
wfsel.sources.esacci_lakes.getters.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.sci.literals                     import FREEZING_POINT_OF_WATER_KELVIN
from wfsel.sources.esacci_lakes.literals    import (
                                                MERGED_PRODUCT_COVERAGE_LOWER_BOUND,
                                                MERGED_PRODUCT_COVERAGE_UPPER_BOUND,
                                            )
from wfsel.sources.esacci_lakes.readers     import read_esacci_lakes_merged_product_csv


def get_all_years(
    esacci_lakes_id:                                            int,
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
) -> list[int]:
    """
    Get all years of a lake by its id.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe

    Returns
    -------
    list[int]
        A list of years
    """
    years   = (
                esacci_lakes_counts_of_distinct_start_days_by_year_df_long[
                    esacci_lakes_counts_of_distinct_start_days_by_year_df_long["esacci_lakes_id"]
                    == esacci_lakes_id
                ]
                ["year"]
                .astype(int)
                .to_list()
            )

    return years


def get_most_recent_year(
    esacci_lakes_id:                                            int,
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
) -> int:
    """
    Get the most recent year of a lake by its id.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe

    Returns
    -------
    int
        A year

    Raises
    ------
    ValueError
        If the unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe contains zero rows labeled by the ESA CCI Lakes
        id
    """
    group   = esacci_lakes_counts_of_distinct_start_days_by_year_df_long[
                esacci_lakes_counts_of_distinct_start_days_by_year_df_long["esacci_lakes_id"]
                == esacci_lakes_id
            ]

    if group.empty:
        message = "expected dataframe to have at least one row"

        raise ValueError(message)

    year    = (
                group
                .sort_values([
                    "year",
                    "count_of_distinct_start_days",
                ])
                .iloc[-1]
                .astype(int)
                ["year"]
            )

    return year


def get_most_smoke_year(
    esacci_lakes_id:                                int,
    counts_of_distinct_start_days_by_year_df_long:  pd.DataFrame,
) -> int:
    """
    Get the most smoke year of a lake by its id.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe

    Returns
    -------
    int
        A year

    Raises
    ------
    ValueError
        If the unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe contains zero rows labeled by the ESA CCI Lakes
        id
    """
    group   = counts_of_distinct_start_days_by_year_df_long[
                counts_of_distinct_start_days_by_year_df_long["esacci_lakes_id"]
                == esacci_lakes_id
            ]

    if group.empty:
        message = "expected dataframe to have at least one row"

        raise ValueError(message)

    year    = (
                group
                .sort_values([
                    "count_of_distinct_start_days",
                    "year",
                ])
                .iloc[-1]
                .astype(int)
                ["year"]
            )

    return year


def get_observations_ser(
    esacci_lakes_id:                        int,
    year:                                   int,
    esacci_lakes_merged_product_dir_path:   Path,
) -> pd.Series[float]:
    """
    Get the observations series of a lake by its id and a year.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    year : int
        The year
    esacci_lakes_merged_product_dir_path : Path
        The ESA CCI Lakes merged product directory path

    Returns
    -------
    pd.Series[float]
        An observation series
    """
    dir_path    = (
                    esacci_lakes_merged_product_dir_path
                    / str(year)
                )

    paths = sorted(dir_path.glob("**/*.csv"))

    _observations = []

    for path in paths:
        merged_product_df = read_esacci_lakes_merged_product_csv(path)

        lake_surface_water_temperature_mean     = float(
            merged_product_df.loc[esacci_lakes_id, "lake_surface_water_temperature_mean"],       # type: ignore[arg-type]
        ) - FREEZING_POINT_OF_WATER_KELVIN
        lake_surface_water_temperature_coverage = float(
            merged_product_df.loc[esacci_lakes_id, "lake_surface_water_temperature_coverage"],   # type: ignore[arg-type]
        )

        if (
                lake_surface_water_temperature_coverage >= MERGED_PRODUCT_COVERAGE_LOWER_BOUND
            and lake_surface_water_temperature_coverage <= MERGED_PRODUCT_COVERAGE_UPPER_BOUND
        ):
            _observations.append(lake_surface_water_temperature_mean)
        else:
            _observations.append(float("nan"))

    observations_ser    = pd.Series(
                            _observations,
                            pd.RangeIndex(
                                1,
                                len(_observations) + 1,
                            ),
                        )

    return observations_ser
