"""
Filename:   wfsel.arguments.py
Author:     William Chuter-Davies
Modified:   10/11/26
"""

# Standard Library Imports
from argparse import ArgumentParser
from pathlib  import Path


def add_argument_force(
    parser: ArgumentParser,
) -> None:
    """
    Add a "force" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-f", "--force",
        action = "store_true",
    )


def add_argument_output(
    parser: ArgumentParser,
) -> None:
    """
    Add a "output" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-o", "--output",
        type        = Path,
        required    = True,
    )
