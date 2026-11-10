"""
Filename:   wfsel.time.arguments.py
Author:     William Chuter-Davies
Modified:   10/11/26
"""

# Standard Library Imports
from argparse   import ArgumentParser
from datetime   import date


def add_argument_date(
    parser: ArgumentParser,
) -> None:
    """
    Add a "date" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "date",
        type = date.fromisoformat,
    )
