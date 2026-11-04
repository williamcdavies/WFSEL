"""
Filename:   wfsel.sources.esa_lakes.readers.py
Author:     William Chuter-Davies
Modified:   03/11/26
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import pandas as pd


def read_esa_lakes_metadata_csv(
    esa_lakes_metadata_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "metadata.csv" (or similar) into a dataframe.

    Parameters
    ----------
    esa_lakes_metadata_csv_path : Path
        The path to "metadata.csv" (or similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            esa_lakes_metadata_csv_path,
            index_col   = "id",
            delimiter   = ";",
        )

    return df


def read_esa_lakes_product_csv(
    esa_lakes_product_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20110101-fv3.0.0.csv" (or
    similar) into a dataframe.

    Parameters
    ----------
    esa_lakes_product_csv_path : Path
        The path to
        "ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20110101-fv3.0.0.csv" (or
        similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            esa_lakes_product_csv_path,
            index_col = "esa_lakes_id",
        )

    return df


def read_esa_lakes_counts_of_distinct_start_days_by_year_csv(
    esa_lakes_counts_of_distinct_start_days_by_year_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "esa_counts_of_distinct_start_days_by_year.csv" (or similar)
    into a dataframe.

    Parameters
    ----------
    esa_lakes_counts_of_distinct_start_days_by_year_csv_path : Path
        The path to "esa_counts_of_distinct_start_days_by_year.csv" (or
        similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            esa_lakes_counts_of_distinct_start_days_by_year_csv_path,
            index_col = "esa_lakes_id",
        )

    return df


def read_esa_lakes_hylak_field_values_csv(
    esa_lakes_hylak_field_values_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "esa_hylak_field_values.csv" (or similar) into a dataframe.

    Parameters
    ----------
    esa_lakes_hylak_field_values_csv_path : Path
        The path to "esa_hylak_field_values.csv" (or similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            esa_lakes_hylak_field_values_csv_path,
            index_col = "esa_lakes_id",
        )

    return df


def read_esa_lakes_high_smoke_year_observations_anomaly_csv(
    esa_lakes_high_smoke_year_observations_anomaly_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "high_smoke_season_lake_surface_water_temperature_anomaly.csv"
    (or similar) into a dataframe.

    Parameters
    ----------
    esa_lakes_high_smoke_year_observations_anomaly_csv_path : Path
        The path to
        "high_smoke_season_lake_surface_water_temperature_anomaly.csv"
        (or similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            esa_lakes_high_smoke_year_observations_anomaly_csv_path,
            index_col = "esa_lakes_id",
        )

    return df


def read_esa_lakes_low_smoke_year_observations_anomaly_csv(
    esa_lakes_low_smoke_year_observations_anomaly_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "low_smoke_season_lake_surface_water_temperature_anomaly.csv"
    (or similar) into a dataframe.

    Parameters
    ----------
    esa_lakes_low_smoke_year_observations_anomaly_csv_path : Path
        The path to
        "low_smoke_season_lake_surface_water_temperature_anomaly.csv"
        (or similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            esa_lakes_low_smoke_year_observations_anomaly_csv_path,
            index_col = "esa_lakes_id",
        )

    return df
