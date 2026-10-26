"""
wfsel.sources.esacci_lakes.melters.

Written by William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd


def melt_esacci_lakes_counts_of_distinct_start_days_by_year_df(
    esacci_lakes_counts_of_distinct_start_days_by_year_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Unpivot an ESA CCI Lakes counts of distinct start days by year
    dataframe from wide format to long format.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_by_year_df : pd.DataFrame
        The ESA CCI Lakes counts of distinct start days by year
        dataframe

    Returns
    -------
    pd.DataFrame
        An unpivoted ESA CCI Lakes counts of distinct start days by year
        dataframe
    """
    df  = (
            esacci_lakes_counts_of_distinct_start_days_by_year_df
            .rename(columns = int)
            .melt(
                var_name        = "year",
                value_name      = "count_of_distinct_start_days",
                ignore_index    = False,
            )
            .reset_index()
        )

    return df
