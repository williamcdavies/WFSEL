"""
Filename:   wfsel.sources.hydro_lakes.arguments.py
Author:     William Chuter-Davies
Modified:   03/11/26
"""

# Standard Library Imports
from argparse import ArgumentParser

# Local Application/Library Specific Imports
from wfsel.sources.hydro_lakes.models import HYLAK_FIELDS


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
        choices = HYLAK_FIELDS.keys(),
    )
