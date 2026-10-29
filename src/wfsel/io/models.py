"""
Filename:   wfsel.io.models.py
Author:     William Chuter-Davies
Modified:   29/10/26
"""

# Standard Library Imports
from dataclasses import dataclass


@dataclass(kw_only = True)
class CompletedProcessLog:
    """Encapsulate a CompletedProcessLog."""

    args:       list[str]
    returncode: int
    stdout:     str
    stderr:     str
