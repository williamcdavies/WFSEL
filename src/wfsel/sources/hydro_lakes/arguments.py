"""
wfsel.sources.hydro_lakes.arguments.

Written by William Chuter-Davies
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
