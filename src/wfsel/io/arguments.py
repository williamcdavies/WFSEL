"""
Filename:   wfsel.io.arguments.py
Author:     William Chuter-Davies
Modified:   29/10/26
"""

# Standard Library Imports
from argparse   import ArgumentParser
from pathlib    import Path


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
