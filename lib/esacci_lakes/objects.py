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
        The variable name, or key, as it appears in the ESA Lakes
        Climate Change Initiative (Lakes_cci): Lake products, Version
        3.0 Product User Guide

    long_name : :class:`str`
        The variable long name

    units : :class:`str`
        The variable units
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
        The field name, or key, as it appears in the HydroLAKES v1.0
        technical documentation

    long_name : :class:`str`
        The field long name

    units : :class:`str`
        The field units

    display_units : :class:`str`
        The display units

    scale : :class:`float` | `None`
        The scale of `units` relative to 1

    display_scale : :class:`float` | `None`
        The scale of `display_units` relative to 1

    lower_bound : :class:`float` | `None`
        The lower bound used to filter lakes by this field. `None` if
        no lower bound applies

    upper_bound : :class:`float` | `None`
        The upper bound used to filter lakes by this field. `None` if
        no upper bound applies
    """
    field_id:      str
    long_name:     str
    units:         str
    display_units: str
    scale:         float | None
    display_scale: float | None
    lower_bound:   float | None
    upper_bound:   float | None
