r"""
objects.py

Description:
   Provides definitions for esacci_lakes-utility classes.

Written by William Chuter-Davies
"""

# Standard Library Imports
from dataclasses import dataclass


@dataclass
class ESACCILakesVariable:
    """
    Dataclass object for representing an ESA CCI Lakes variable.

    Parameters
    ----------
    var_id : :class:`str`
        Variable name, or key, as it appears in the ESA Lakes Climate
        Change Initiative (Lakes_cci): Lake products, Version 3.0
        Product User Guide

    long_name : :class:`str`
        Variable long name

    units : :class:`str`
        Variable units
    """
    var_id:    str
    long_name: str
    units:     str


@dataclass
class HylakField:
    """
    Dataclass object for representing a HydroLAKES field.

    Parameters
    ----------
    field_id : :class:`str`
        Field name, or key, as it appears in the HydroLAKES v1.0
        technical documentation

    long_name : :class:`str`
        Field long name

    units : :class:`str`
        Field units

    display_units : :class:`str`
        Units to display `lower_bound`/`upper_bound` in.

    scale : float | None
        The scale of `units` relative to 1.

    display_scale : float | None
        The scale of 'display_units' relative to 1.

    lower_bound : float | None
        Lower bound used to filter lakes by this field. `None` if no
        lower bound applies.

    upper_bound : float | None
        Upper bound used to filter lakes by this field. `None` if no
        upper bound applies.
    """
    field_id:      str
    long_name:     str
    units:         str
    display_units: str
    scale:         float | None
    display_scale: float | None
    lower_bound:   float | None
    upper_bound:   float | None
