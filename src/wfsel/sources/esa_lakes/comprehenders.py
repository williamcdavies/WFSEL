"""
Filename:   wfsel.sources.esa_lakes.comprehenders.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.sources.esa_lakes.getters import get_observations_ser


def comprehend_observations_ser_list(
    esa_lakes_id:               int,
    years:                      list[int],
    esa_lakes_product_dir_path: Path,
) -> list[pd.Series[float]]:
    """
    Comprehend a list of observations series.

    Parameters
    ----------
    esa_lakes_id : int
        The ESA Lakes id
    years : list[int]
        The list of years
    esa_lakes_product_dir_path : Path
        The ESA Lakes product directory path

    Returns
    -------
    list[pd.Series[float]]
        A list of observations series
    """
    observations_ser_list   = [
                                get_observations_ser(
                                    esa_lakes_id,
                                    year,
                                    esa_lakes_product_dir_path,
                                )
                                for year
                                in years
                            ]

    return observations_ser_list


def comprehend_esa_lakes_column_name_list(
    esa_lakes_week_first:   int,
    esa_lakes_week_last:    int,
) -> list[str]:
    """
    Comprehend a list of ESA Lakes column names.

    Parameters
    ----------
    esa_lakes_week_first : int
        The first week
    esa_lakes_week_last : int
        The last week

    Returns
    -------
    list[str]
        A list of column names
    """
    column_name_list    = [
                            f"w_{i}"
                            for i
                            in range(
                                esa_lakes_week_first,
                                esa_lakes_week_last + 1,
                            )
                        ]

    return column_name_list
