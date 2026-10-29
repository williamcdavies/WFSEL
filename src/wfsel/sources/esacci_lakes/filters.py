"""
Filename:   wfsel.sources.esacci_lakes.filters.py
Author:     William Chuter-Davies
Modified:   29/10/26
"""

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.sources.esacci_lakes.literals    import (
                                                COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND,
                                                COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND,
                                            )


def filter_counts_of_distinct_start_days_by_year_df_long_by_upper_bound(
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
) -> pd.DataFrame:
    """
    Filter an unpivoted ESA CCI Lakes counts of distinct start days by
    year dataframe by the upper bound.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe

    Returns
    -------
    pd.DataFrame
        A filtered unpivoted ESA CCI Lakes counts of distinct start days
        by year dataframe
    """
    df  = esacci_lakes_counts_of_distinct_start_days_by_year_df_long[
            esacci_lakes_counts_of_distinct_start_days_by_year_df_long["count_of_distinct_start_days"]
            >= COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND
        ]

    return df


def filter_counts_of_distinct_start_days_by_year_df_long_by_lower_bound(
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long: pd.DataFrame,
) -> pd.DataFrame:
    """
    Filter an unpivoted ESA CCI Lakes counts of distinct start days by
    year dataframe by the lower bound.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
        The unpivoted ESA CCI Lakes counts of distinct start days by
        year dataframe

    Returns
    -------
    pd.DataFrame
        A filtered unpivoted ESA CCI Lakes counts of distinct start days
        by year dataframe
    """
    df  = esacci_lakes_counts_of_distinct_start_days_by_year_df_long[
            esacci_lakes_counts_of_distinct_start_days_by_year_df_long["count_of_distinct_start_days"]
            <= COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND
        ]

    return df
