"""
wfsel.sources.esacci_lakes.arguments.

Written by William Chuter-Davies
"""

# Standard Library Imports
from argparse   import ArgumentParser
from pathlib    import Path


def add_argument_esacci_lakes_id(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esacci_lakes_id" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_id",
        type = int,
    )


def add_argument_esacci_lakes_metadata_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esacci_lakes_metadata_csv_path" argument to a parser.

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
    Add a "esacci_lakes_static_lake_mask_nc_path" argument to a parser.

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
    Add a "esacci_lakes_merged_product_nc_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_merged_product_nc_path",
        type = Path,
    )


def add_argument_esacci_lakes_merged_product_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esacci_lakes_merged_product_csv_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_merged_product_csv_path",
        type = Path,
    )


def add_argument_esacci_lakes_merged_product_dir_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esacci_lakes_merged_product_dir_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_merged_product_dir_path",
        type = Path,
    )


def add_argument_esacci_lakes_counts_of_distinct_start_days_by_year_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esacci_lakes_counts_of_distinct_start_days_by_year_csv_path"
    argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "esacci_lakes_counts_of_distinct_start_days_by_year_csv_path",
        type = Path,
    )


def add_argument_esacci_lakes_hylak_field_values_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esacci_lakes_hylak_field_values_csv_path" argument to a
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
