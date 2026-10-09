r"""
objects.py

Description:
    Provides definitions for proc-utility classes.

Written by William Chuter-Davies
"""

# Standard Library Imports
from dataclasses import dataclass


# Dataclasses
# ==================================================================================================
@dataclass
class CompletedProcessLog:
    """
    Encapsulates the output of a subprocess.

    Parameters
    ----------
    args : list[:class:`str`]
        The command and arguments passed to a subprocess

    returncode : :class:`int`
        The exit code returned by a subprocess

    stdout : :class:`str`
        The captured standard output from a subprocess

    stderr : :class:`str`
        The captured standard error from a subprocess
    """
    args:       list[str]
    returncode: int
    stdout:     str
    stderr:     str


# ==================================================================================================
