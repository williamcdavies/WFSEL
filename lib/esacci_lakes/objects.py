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
