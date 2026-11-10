"""
Filename:   wfsel.sources.esa_lakes.getters.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path
from typing  import Literal

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.sci.literals                 import FREEZING_POINT_OF_WATER_KELVIN
from wfsel.sources.esa_lakes.literals   import (
                                            ESA_LAKES_PRODUCT_COVERAGE_LOWER_BOUND,
                                            ESA_LAKES_PRODUCT_COVERAGE_UPPER_BOUND,
                                        )
from wfsel.sources.esa_lakes.readers    import read_esa_lakes_product_csv
from wfsel.io.finders                   import find_file_paths_by_extension


def get_all_years(
    esa_lakes_id:                                               int,
    esa_lakes_counts_of_distinct_start_days_by_year_df_long:    pd.DataFrame,
) -> list[int]:
    """
    Get all years of a lake by its id.

    Parameters
    ----------
    esa_lakes_id : int
        The ESA Lakes id
    esa_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA Lakes counts of distinct start days by year
        dataframe

    Returns
    -------
    list[int]
        A list of years
    """
    years   = (
                esa_lakes_counts_of_distinct_start_days_by_year_df_long[
                    esa_lakes_counts_of_distinct_start_days_by_year_df_long["esa_lakes_id"]
                    == esa_lakes_id
                ]
                ["year"]
                .astype(int)
                .to_list()
            )

    return years


def _get_year_by_sort(
    esa_lakes_id:                                               int,
    esa_lakes_counts_of_distinct_start_days_by_year_df_long:    pd.DataFrame,
    sort_by:                                                    Literal["recent", "smoke"],
) -> int:
    """
    Get a year of a lake by its id and a sort strategy.

    Parameters
    ----------
    esa_lakes_id : int
        The ESA Lakes id
    esa_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA Lakes counts of distinct start days by year
        dataframe
    sort_by : Literal["recent", "smoke"]
        The sort strategy

    Returns
    -------
    int
        A year

    Raises
    ------
    ValueError
        If the unpivoted ESA Lakes counts of distinct start days by year
        dataframe contains zero rows labeled by the ESA Lakes id
    """
    group   = esa_lakes_counts_of_distinct_start_days_by_year_df_long[
                esa_lakes_counts_of_distinct_start_days_by_year_df_long["esa_lakes_id"]
                == esa_lakes_id
            ]

    if group.empty:
        message = "expected dataframe to have at least one row"

        raise ValueError(message)

    match sort_by:
        case "recent":
            sort_columns = ["year", "count_of_distinct_start_days"]
        case "smoke":
            sort_columns = ["count_of_distinct_start_days", "year"]

    year    = (
                group
                .sort_values(sort_columns)
                .iloc[-1]
                .astype(int)
                ["year"]
            )

    return year


def get_most_recent_year(
    esa_lakes_id:                                               int,
    esa_lakes_counts_of_distinct_start_days_by_year_df_long:    pd.DataFrame,
) -> int:
    """
    Get the most recent year of a lake by its id.

    Parameters
    ----------
    esa_lakes_id : int
        The ESA Lakes id
    esa_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA Lakes counts of distinct start days by year
        dataframe

    Returns
    -------
    int
        A most recent year

    Raises
    ------
    ValueError
        If the unpivoted ESA Lakes counts of distinct start days by year
        dataframe contains zero rows labeled by the ESA Lakes id
    """
    year = _get_year_by_sort(
        esa_lakes_id,
        esa_lakes_counts_of_distinct_start_days_by_year_df_long,
        "recent",
    )

    return year


def get_most_smoke_year(
    esa_lakes_id:                                               int,
    esa_lakes_counts_of_distinct_start_days_by_year_df_long:    pd.DataFrame,
) -> int:
    """
    Get the most smoke year of a lake by its id.

    Parameters
    ----------
    esa_lakes_id : int
        The ESA Lakes id
    esa_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA Lakes counts of distinct start days by year
        dataframe

    Returns
    -------
    int
        A most smoke year

    Raises
    ------
    ValueError
        If the unpivoted ESA Lakes counts of distinct start days by year
        dataframe contains zero rows labeled by the ESA Lakes id
    """
    year = _get_year_by_sort(
        esa_lakes_id,
        esa_lakes_counts_of_distinct_start_days_by_year_df_long,
        "smoke",
    )

    return year


def get_observations_ser(
    esa_lakes_id:               int,
    year:                       int,
    esa_lakes_product_dir_path: Path,
) -> pd.Series[float]:
    """
    Get an observations series of a lake by its id and a year.

    Parameters
    ----------
    esa_lakes_id : int
        The ESA Lakes id
    year : int
        The year
    esa_lakes_product_dir_path : Path
        The ESA Lakes product directory path

    Returns
    -------
    pd.Series[float]
        An observations series
    """
    dir_path    = esa_lakes_product_dir_path / str(year)
    file_paths  = find_file_paths_by_extension(dir_path, "csv")

    observations_ser_list = []

    for file_path in file_paths:
        product_df = read_esa_lakes_product_csv(file_path)

        lake_surface_water_temperature_mean     = float(
            product_df.loc[esa_lakes_id, "lake_surface_water_temperature_mean"],        # type: ignore[arg-type]
        ) - FREEZING_POINT_OF_WATER_KELVIN
        lake_surface_water_temperature_coverage = float(
            product_df.loc[esa_lakes_id, "lake_surface_water_temperature_coverage"],    # type: ignore[arg-type]
        )

        if (
                lake_surface_water_temperature_coverage >= ESA_LAKES_PRODUCT_COVERAGE_LOWER_BOUND
            and lake_surface_water_temperature_coverage <= ESA_LAKES_PRODUCT_COVERAGE_UPPER_BOUND
        ):
            observations_ser_list.append(lake_surface_water_temperature_mean)
        else:
            observations_ser_list.append(float("nan"))

    observations_ser    = pd.Series(
                            observations_ser_list,
                            pd.RangeIndex(
                                1,
                                len(observations_ser_list) + 1,
                            ),
                        )

    return observations_ser
