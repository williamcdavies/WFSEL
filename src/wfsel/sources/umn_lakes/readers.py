"""
Filename:   wfsel.sources.umn_lakes.readers.py
Author:     William Chuter-Davies
Modified:   06/11/26
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import pandas as pd


def read_umn_lakes_product_tsv(
    umn_lakes_product_csv_path: Path,
) -> pd.DataFrame:
    """
    Read "S2MSI1C_MN_2017_2m0iA4.tsv" (or
    similar) into a dataframe.

    Parameters
    ----------
    umn_lakes_product_csv_path : Path
        The path to
        "S2MSI1C_MN_2017_2m0iA4.tsv" (or
        similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            umn_lakes_product_csv_path,
            index_col   = [
                            "Field",
                            "Date",
                            "unmlknum",
                        ],
            delimiter   = "\t",
        )

    return df
