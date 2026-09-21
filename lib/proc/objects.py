r"""
objects.py

Description:
    Provides definitions for proc-utility classes.

Written by William Chuter-Davies
"""

# Standard Library Imports
from dataclasses import dataclass


@dataclass
class CompletedProcessLog:
    """
    Dataclass object for encapsulating the output of `subprocess.run`.

    Parameters
    ----------
    args : :class:`list`
        The command and arguments passed to `subprocess.run`

    returncode : :class:`int`
        The exit code returned by `subprocess.run`

    stdout : :class:`str`
        The captured standard output from `subprocess.run`

    stderr : :class:`str`
        The captured standard error from `subprocess.run`
    """
    args:       list
    returncode: int
    stdout:     str
    stderr:     str
