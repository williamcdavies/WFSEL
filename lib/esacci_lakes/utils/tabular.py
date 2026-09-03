r"""
tabular.py

Description:
   Provides definitions for esacci_lakes-utility tabular functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import pandas as pd


def read_esacci_lakes_metadata_csv(
    esacci_lakes_metadata_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_metadata_csv_path` into a
    :class:`pandas.DataFrame`.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The path to the `lakescci_v2.1.0_metadata.csv` file as provided
        by ESA Lakes Climate Change Initiative (Lakes_cci): Lake
        products, Version 3.0

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_metadata_csv_path,
        delimiter=";",
        index_col="id"
    )


def read_esacci_lakes_average_depths_csv(
    esacci_lakes_average_depths_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_average_depths_csv_path` into a
    :class:`pandas.DataFrame`.

    Parameters
    ----------
    esacci_lakes_average_depths_csv_path : :class:`pathlib.Path`
        The path to some average depths data csv file as produced by
        query_esacci_lakes_average_depths.sql

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_average_depths_csv_path,
        index_col="esacci_lakes_id"
    )


def read_esacci_lakes_counts_of_distinct_start_days_csv(
    esacci_lakes_counts_of_distinct_start_days_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_counts_of_distinct_start_days_csv_path` into a
    :class:`pandas.DataFrame`.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_csv_path : :class:`pathlib.Path`
        The path to some counts of distinct start days data csv file as
        produced by
        query_esacci_lakes_for_counts_of_distinct_start_days.sql

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_counts_of_distinct_start_days_csv_path,
        index_col="esacci_lakes_id"
    )


def read_esacci_lakes_hylak_ids_csv(
    esacci_lakes_hylak_ids_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_hylak_ids_csv_path` into a
    :class:`pandas.DataFrame`.

    Parameters
    ----------
    esacci_lakes_hylak_ids_csv_path : :class:`pathlib.Path`
        The path to some hylaks ids data csv file as produced by
        query_esacci_lakes_for_hylak_ids.sql

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_hylak_ids_csv_path,
        index_col="esacci_lakes_id"
    )
