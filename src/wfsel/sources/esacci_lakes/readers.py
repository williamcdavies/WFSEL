"""
wfsel.sources.esacci_lakes.readers.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import pandas as pd


def read_esacci_lakes_metadata_csv(
    esacci_lakes_metadata_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "metadata.csv" (or similar) into a dataframe.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : Path
        The path to "metadata.csv" (or similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df = pd.read_csv(
        esacci_lakes_metadata_csv_path,
        delimiter   = ";",
        index_col   = "id",
    )

    return df


def read_esacci_lakes_merged_product_csv(
    esacci_lakes_merged_product_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20110101-fv3.0.0.csv" (or
    similar) into a dataframe.

    Parameters
    ----------
    esacci_lakes_merged_product_csv_path : Path
        The path to
        "ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20110101-fv3.0.0.csv" (or
        similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df = pd.read_csv(
        esacci_lakes_merged_product_csv_path,
        index_col = "esacci_lakes_id",
    )

    return df


def read_esacci_lakes_counts_of_distinct_start_days_by_year_csv(
    esacci_lakes_counts_of_distinct_start_days_by_year_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "counts_of_distinct_start_days_by_year.csv" (or similar) into a
    dataframe.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_by_year_csv_path : Path
        The path to "counts_of_distinct_start_days_by_year.csv" (or
        similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df = pd.read_csv(
        esacci_lakes_counts_of_distinct_start_days_by_year_csv_path,
        index_col = "esacci_lakes_id",
    )

    return df


def read_esacci_lakes_hylak_field_values_csv(
    esacci_lakes_hylak_field_values_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "hylak_field_values.csv" (or similar) into a dataframe.

    Parameters
    ----------
    esacci_lakes_hylak_field_values_csv_path : Path
        The path to "hylak_field_values.csv" (or similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df = pd.read_csv(
        esacci_lakes_hylak_field_values_csv_path,
        index_col = "esacci_lakes_id",
    )

    return df
