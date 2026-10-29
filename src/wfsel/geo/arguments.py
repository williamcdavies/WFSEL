"""
Filename:   wfsel.geo.arguments.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Standard Library Imports
from argparse import ArgumentParser


def add_argument_stusps(
    parser: ArgumentParser,
) -> None:
    """
    Add a "stusps" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "stusps",
        type    = str,
        nargs   = "+",
    )
