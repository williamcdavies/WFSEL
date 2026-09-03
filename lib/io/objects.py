r"""
objects.py

Description:
   Provides definitions for io-utility classes.

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
        `subprocess.run.args`

    returncode : :class:`int`
        `subprocess.run.returncode`

    stdout : :class:`str`
        `subprocess.run.stdout`

    stderr : :class:`str`
        `subprocess.run.stderr`
    """
    args:       list
    returncode: int
    stdout:     str
    stderr:     str
