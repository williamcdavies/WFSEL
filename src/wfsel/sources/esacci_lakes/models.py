"""
Filename:   wfsel.sources.esacci_lakes.models.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Standard Library Imports
from dataclasses import dataclass

# Related Third-party Imports
import pandas as pd


@dataclass(kw_only = True)
class ESACCILakesVariable:
    """Encapsulate a ESACCILakesVariable."""

    var_id:     str
    long_name:  str
    units:      str

ESACCI_LAKES_VARIABLES  = {
                            "lake_surface_water_temperature":
                            ESACCILakesVariable(
                                var_id      = "lake_surface_water_temperature",
                                long_name   = "Lake Surface Skin Temperature",
                                units       = "K",
                            ),
                        }


@dataclass(kw_only = True)
class Season:
    """
    Encapsulate a Season.

    Raises
    ------
    ValueError
        If the index of the observations series is not [1,
        len(observations series)]
    ValueError
        If first is not in [1, len(observations series)]
    ValueError
        If last is not in [1, len(observations series)]
    ValueError
        If first is greater than last
    """

    observations_ser:   pd.Series[float]
    first:              int
    last:               int

    def __post_init__(
        self,
    ) -> None:
        """
        Perform post-initialisation checks.

        Raises
        ------
        ValueError
            If the index of the observations series is not [1,
            len(observations series)]
        ValueError
            If first is not in [1, len(observations series)]
        ValueError
            If last is not in [1, len(observations series)]
        ValueError
            If first is greater than last
        """
        actual      = self.observations_ser.index
        expected    = pd.RangeIndex(
                        1,
                        len(self.observations_ser) + 1,
                    )

        if not actual.equals(expected):
            message = f"expected index to be [1, {len(self.observations_ser)}]: got {actual.tolist()}"

            raise ValueError(message)

        if self.first not in actual:
            message = f"expected first ({self.first}) to be in [1, {len(self.observations_ser)}]"

            raise ValueError(message)

        if self.last not in actual:
            message = f"expected last ({self.last}) to be in [1, {len(self.observations_ser)}]"

            raise ValueError(message)

        if self.first > self.last:
            message =  f"expected first ({self.first}) to be less than or equal to last ({self.last})"

            raise ValueError(message)
