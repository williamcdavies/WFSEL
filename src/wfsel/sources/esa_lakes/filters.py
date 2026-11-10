"""
Filename:   wfsel.sources.esa_lakes.filters.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.sources.esa_lakes.literals   import (
                                            ESA_LAKES_COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND,
                                            ESA_LAKES_COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND,
                                        )


def filter_counts_of_distinct_start_days_by_year_df_long_by_upper_bound(
    esa_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
) -> pd.DataFrame:
    """
    Filter an unpivoted ESA Lakes counts of distinct start days by year
    dataframe by the upper bound.

    Parameters
    ----------
    esa_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA Lakes counts of distinct start days by year
        dataframe

    Returns
    -------
    pd.DataFrame
        A filtered unpivoted ESA Lakes counts of distinct start days by
        year dataframe
    """
    df  = esa_lakes_counts_of_distinct_start_days_by_year_df_long[
            esa_lakes_counts_of_distinct_start_days_by_year_df_long["count_of_distinct_start_days"]
            >= ESA_LAKES_COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
        ]

    return df


def filter_counts_of_distinct_start_days_by_year_df_long_by_lower_bound(
    esa_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
) -> pd.DataFrame:
    """
    Filter an unpivoted ESA Lakes counts of distinct start days by year
    dataframe by the lower bound.

    Parameters
    ----------
    esa_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA Lakes counts of distinct start days by year
        dataframe

    Returns
    -------
    pd.DataFrame
        A filtered unpivoted ESA Lakes counts of distinct start days by
        year dataframe
    """
    df  = esa_lakes_counts_of_distinct_start_days_by_year_df_long[
            esa_lakes_counts_of_distinct_start_days_by_year_df_long["count_of_distinct_start_days"]
            <= ESA_LAKES_COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND
        ]

    return df
