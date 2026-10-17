"""
wfsel.sources.esacci_lakes.readers.

Written by William Chuter-Davies
"""

# Standard Library Imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

# Related Third-party Imports
import pandas as pd


def read_esacci_lakes_metadata_csv(
    esacci_lakes_metadata_csv_path: Path,
) -> pd.DataFrame:
    """
    Read `lakescci_v2.1.0_metadata.csv` (or similar) into a DataFrame.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : Path
        The path to `lakescci_v2.1.0_metadata.csv` (or similar)

    Returns
    -------
    pd.DataFrame

    """
    df = pd.read_csv(
        esacci_lakes_metadata_csv_path,
        delimiter = ";",
        index_col = "id",
    )

    return df


def read_esacci_lakes_hylak_field_values_csv(
    esacci_lakes_hylak_field_values_csv_path: Path,
) -> pd.DataFrame:
    """
    Read `esacci_lakes_hylak_field_values.csv` (or similar) into a
    DataFrame.

    Parameters
    ----------
    esacci_lakes_hylak_field_values_csv_path : Path
        The path to `esacci_lakes_hylak_field_values.csv` (or similar)

    Returns
    -------
    pd.DataFrame

    """
    df = pd.read_csv(
        esacci_lakes_hylak_field_values_csv_path,
        index_col = "esacci_lakes_id",
    )

    return df
