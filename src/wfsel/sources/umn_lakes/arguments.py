"""
Filename:   wfsel.sources.umn_lakes.arguments.py
Author:     William Chuter-Davies
Modified:   10/11/26
"""

# Standard Library Imports
from argparse   import ArgumentParser
from pathlib    import Path


def add_argument_umn_lakes_id(
    parser: ArgumentParser,
) -> None:
    """
    Add a "umn_lakes_id" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "umn_lakes_id",
        type = str,
    )


def add_argument_umn_lakes_product_tsv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "umn_lakes_product_tsv_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "umn_lakes_product_tsv_path",
        type = Path,
    )


def add_argument_umn_lakes_product_dir_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "umn_lakes_product_dir_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "umn_lakes_product_dir_path",
        type = Path,
    )
