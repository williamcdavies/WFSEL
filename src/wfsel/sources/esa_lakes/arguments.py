"""
Filename:   wfsel.sources.esa_lakes.arguments.py
Author:     William Chuter-Davies
"""

# Standard Library Imports
from argparse   import ArgumentParser
from pathlib    import Path


def add_argument_esa_lakes_id(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_id" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_id",
        type    = int,
        metavar = "INT",
    )


def add_argument_esa_lakes_metadata_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_metadata_csv_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_metadata_csv_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_static_lake_mask_nc_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_static_lake_mask_nc_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_static_lake_mask_nc_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_product_nc_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_product_nc_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_product_nc_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_product_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_product_csv_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_product_csv_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_product_dir_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_product_dir_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_product_dir_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_counts_of_distinct_start_days_by_year_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_counts_of_distinct_start_days_by_year_csv_path"
    argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_counts_of_distinct_start_days_by_year_csv_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_hylak_field_values_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_hylak_field_values_csv_path" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_hylak_field_values_csv_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_high_smoke_year_observations_anomaly_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_high_smoke_year_observations_anomaly_csv_path"
    argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_high_smoke_year_observations_anomaly_csv_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_low_smoke_year_observations_anomaly_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_low_smoke_year_observations_anomaly_csv_path"
    argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "esa_lakes_low_smoke_year_observations_anomaly_csv_path",
        type    = Path,
        metavar = "PATH",
    )


def add_argument_esa_lakes_week_first(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_week_first" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-wf", "--esa-lakes-week-first",
        type        = int,
        required    = False,
        metavar     = "INT",
        default     = 1,
    )


def add_argument_esa_lakes_week_last(
    parser: ArgumentParser,
) -> None:
    """
    Add a "esa_lakes_week_last" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "-wl", "--esa-lakes-week-last",
        type        = int,
        required    = False,
        metavar     = "INT",
        default     = 20,
    )
