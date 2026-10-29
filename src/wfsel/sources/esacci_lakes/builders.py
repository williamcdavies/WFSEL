"""
Filename:   wfsel.sources.esacci_lakes.builders.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Related Third-party Imports
import pandas as pd


def build_distinct_labels_mask(
    distinct_labels_ser:    pd.Series[int],
    start:                  int,
    stop:                   int,
) -> pd.Series[int]:
    """
    Build a distinct labels mask.

    Parameters
    ----------
    distinct_labels_ser : pd.Series[int]
        The distinct labels series
    start : int
        The start of the range index, inclusive
    stop : int
        The stop of the range index, exclusive

    Returns
    -------
    pd.Series[int]
        A distinct labels mask
    """
    mask    = pd.Series(
                0,
                pd.RangeIndex(
                    start,
                    stop,
                ),
            )

    mask.loc[distinct_labels_ser] = 1

    return mask
