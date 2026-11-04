"""
Filename:   wfsel.math.arguments.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Standard Library Imports
from argparse import ArgumentParser

# Local Application/Library Specific Imports
from wfsel.math.literals import SCALES


def add_argument_scale(
    parser: ArgumentParser,
) -> None:
    """
    Add a "scale" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-s", "--scale",
        type    = str,
        choices = SCALES,
        default = "linear",
    )
