"""
Filename:   wfsel.geo.arguments.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Standard Library Imports
from argparse import ArgumentParser

# Local Application/Library Specific Imports
from wfsel.geo.literals import TWO_LETTER_STATE_AND_POSSESSION_ABBREVIATIONS


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
        "-s", "--stusps",
        type        = str,
        nargs       = "+",
        choices     = TWO_LETTER_STATE_AND_POSSESSION_ABBREVIATIONS.keys(),
        default     = "NV",
    )
