"""
wfsel.sources.esacci_lakes.arguments.

Written by William Chuter-Davies
"""

# Standard Library Imports
from pathlib import Path
from typing  import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import ArgumentParser


def add_argument_esacci_lakes_metadata_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a `esacci_lakes_metadata_csv_path` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_metadata_csv_path",
        type = Path,
    )


def add_argument_esacci_lakes_static_lake_mask_nc_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a `esacci_lakes_static_lake_mask_nc_path` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_static_lake_mask_nc_path",
        type = Path,
    )


def add_argument_esacci_lakes_merged_product_nc_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a `esacci_lakes_merged_product_nc_path` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_merged_product_nc_path",
        type = Path,
    )


def add_argument_esacci_lakes_merged_product_dir_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a `esacci_lakes_merged_product_dir_path` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_merged_product_dir_path",
        type = Path,
    )


def add_argument_esacci_lakes_hylak_field_values_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a `esacci_lakes_hylak_field_values_csv_path` argument to a
    parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_hylak_field_values_csv_path",
        type = Path,
    )
