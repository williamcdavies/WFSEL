"""
Filename:   wfsel.sources.hydro_lakes.arguments.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Standard Library Imports
from argparse import ArgumentParser


def add_argument_hylak_field(
    parser: ArgumentParser,
) -> None:
    """
    Add a "hylak_field" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "hylak_field",
        type = str,
    )
