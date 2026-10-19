"""
wfsel.math.arguments.

Written by William Chuter-Davies
"""

# Standard Library Imports
from argparse import ArgumentParser


def add_argument_scale(
    parser: ArgumentParser,
) -> None:
    """
    Add a 'scale' argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-s", "--scale",
        type     = str,
        required = True,
    )
