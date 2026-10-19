"""
wfsel.io.models.

Written by William Chuter-Davies
"""

# Standard Library Imports
from dataclasses import dataclass


@dataclass(kw_only = True)
class CompletedProcessLog:
    """Encapsualtes CompletedProcessLog."""

    args:       list[str]
    returncode: int
    stdout:     str
    stderr:     str
