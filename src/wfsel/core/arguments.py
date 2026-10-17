"""
wfsel.core.arguments.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path
from typing  import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import ArgumentParser


def add_argument_output(
    parser: ArgumentParser,
) -> None:
    """
    Add a `output` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-o", "--output",
        type     = Path,
        required = True,
    )
