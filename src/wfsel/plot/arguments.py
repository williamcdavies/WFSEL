"""
Filename:   wfsel.plot.arguments.py
Author:     William Chuter-Davies
Modified:   03/11/26
"""

# Standard Library Imports
from argparse import ArgumentParser


def add_argument_dimension(
    parser: ArgumentParser,
) -> None:
    """
    Add a "dimension" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-d", "--dimension",
        type    = int,
        choices = [2, 3],
        default = 2,
    )


def add_argument_elevation(
    parser: ArgumentParser,
) -> None:
    """
    Add a "elevation" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-e", "--elevation",
        type    = float,
        default = 45,
    )


def add_argument_azimuth(
    parser: ArgumentParser,
) -> None:
    """
    Add a "azimuth" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-a", "--azimuth",
        type    = float,
        default = 45,
    )
