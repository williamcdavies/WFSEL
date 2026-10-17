"""
wfsel.core.pandas_utils.

Written by William Chuter-Davies
"""

# Standard Library Imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

# Related Third-party Imports
if TYPE_CHECKING:
    import pandas as pd


def to_csv(
    df:               pd.DataFrame,
    output_file_path: Path,
) -> None:
    """
    Write a DataFrame to a .csv file.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame
    output_file_path : Path
        The output file path
    """
    output_file_path.parent.mkdir(
        parents  = True,
        exist_ok = True,
    )

    df.to_csv(output_file_path)


def compute_quantiles(
    ser:    pd.Series,
    levels: list[float],
) -> list[float]:
    """
    Compute the quantiles of a Series.

    Parameters
    ----------
    ser : pd.Series
        The Series
    levels : list[float]
        The list of levels

    Returns
    -------
    list[float]
    """
    quantiles = [
        float(ser.quantile(level))
        for level
        in levels
    ]

    return quantiles
