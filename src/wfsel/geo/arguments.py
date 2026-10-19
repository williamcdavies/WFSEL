"""
wfsel.geo.arguments.

Written by William Chuter-Davies
"""

# Standard Library Imports
from argparse import ArgumentParser


def add_argument_stusps(
    parser: ArgumentParser,
) -> None:
    """
    Add a `stusps` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "stusps",
        nargs = "+",
        type  = str,
    )
