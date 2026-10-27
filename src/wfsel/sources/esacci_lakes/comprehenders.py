"""
wfsel.sources.esacci_lakes.comprehenders.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.sources.esacci_lakes.getters import get_observations_ser


def comprehend_observations(
    esacci_lakes_id:                        int,
    years:                                  list[int],
    esacci_lakes_merged_product_dir_path:   Path,
) -> list[pd.Series]:
    """
    Comprehend a list of observation series.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    years : list[int]
        The list of years
    esacci_lakes_merged_product_dir_path : Path
        The ESA CCI Lakes merged product directory path

    Returns
    -------
    list[pd.Series]
        A list of observation series
    """
    observations    = [
                        get_observations_ser(
                            esacci_lakes_id,
                            year,
                            esacci_lakes_merged_product_dir_path,
                        )
                        for year
                        in years
                    ]

    return observations
