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
    """

    var_id:    str
    long_name: str
    units:     str