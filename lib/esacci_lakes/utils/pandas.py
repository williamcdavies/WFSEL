r"""
argparse.py

Description:
   Provides definitions for esacci_lakes-utility pandas functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import pandas as pd


def read_esacci_lakes_metadata_csv(
    esacci_lakes_metadata_csv_path: Path,
) -> pd.DataFrame:
    return pd.read_csv(
        esacci_lakes_metadata_csv_path,
        delimiter=";",
        index_col="id",
    )


def read_esacci_lakes_average_depths_csv(
    esacci_lakes_average_depths_csv_path: Path,
) -> pd.DataFrame:
    return pd.read_csv(
        esacci_lakes_average_depths_csv_path,
        index_col="esacci_lakes_id",
    )


def read_esacci_lakes_counts_of_distinct_start_days_csv(
    esacci_lakes_counts_of_distinct_start_days_csv_path: Path,
) -> pd.DataFrame:
    return pd.read_csv(
        esacci_lakes_counts_of_distinct_start_days_csv_path,
        index_col="esacci_lakes_id",
    )


def read_esacci_lakes_hylak_ids_csv(
    esacci_lakes_hylak_ids_csv_path: Path,
) -> pd.DataFrame:
    return pd.read_csv(
        esacci_lakes_hylak_ids_csv_path,
        index_col="esacci_lakes_id",
    )
