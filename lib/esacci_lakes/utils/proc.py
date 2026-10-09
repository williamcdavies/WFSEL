r"""
proc.py

Description:
    Provides definitions for esacci_lakes-utility proc functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from datetime import datetime
from pathlib  import Path

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from lib.esacci_lakes.vars import (
    ESACCI_LAKES_VARIABLES,
    HYLAK_FIELDS
)


# Parser functions
# ==================================================================================================
def add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_counts_of_distinct_start_days_csv_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `esacci_lakes_counts_of_distinct_start_days_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_counts_of_distinct_start_days_csv_path",
        type = Path,
        help = "path to some counts of distinct start days data csv file as produced by query_esacci_lakes_for_counts_of_distinct_start_days.sql"
    )


def add_argument_esacci_lakes_hylak_fields_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_hylak_fields_csv_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `esacci_lakes_hylak_fields_csv_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_hylak_fields_csv_path",
        type = Path,
        help = "path to some hylak fields data csv file as produced by query_esacci_lakes_for_hylak_fields.sql"
    )


def add_argument_esacci_lakes_id(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_id` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `esacci_lakes_id` is of type :class:`int`.
    """
    parser.add_argument(
        "esacci_lakes_id",
        type = int,
        help = "esacci_lakes_id as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0"
    )


def add_argument_esacci_lakes_merged_product_dir_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_merged_product_dir_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `esacci_lakes_merged_product_dir_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_merged_product_dir_path",
        type = Path,
        help = "path to the ESA CCI merged_product directory as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0"
    )


def add_argument_esacci_lakes_merged_product_nc_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_merged_product_nc_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `esacci_lakes_merged_product_nc_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_merged_product_nc_path",
        type = Path,
        help = "path to some `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0"
    )


def add_argument_esacci_lakes_metadata_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_metadata_csv_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `esacci_lakes_metadata_csv_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_metadata_csv_path",
        type = Path,
        help = "path to the `lakescci_v2.1.0_metadata.csv` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0"
    )


def add_argument_esacci_lakes_static_lake_mask_nc_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_static_lake_mask_nc_path` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `esacci_lakes_static_lake_mask_nc_path` is of type
    :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_static_lake_mask_nc_path",
        type = Path,
        help = "path to the `ESA_CCI_static_lake_mask.nc` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0"
    )


def add_argument_esacci_lakes_variable(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_variable` argument to a
    :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `esacci_lakes_variable` is of type :class:`str`.
    """
    parser.add_argument(
        "esacci_lakes_variable",
        type = str,
        help = f"one of {", ".join(ESACCI_LAKES_VARIABLES)}"
    )


def add_argument_hylak_field(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `hylak_field` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `hylak_field` is of type :class:`str`.
    """
    parser.add_argument(
        "hylak_field",
        type = str,
        help = f"one of {", ".join(HYLAK_FIELDS)}"
    )


def add_argument_local_data_dir_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `local_data_dir_path` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None.

    Notes
    -----
    Argument `local_data_dir_path` is of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "local_data_dir_path",
        type = Path,
        help = "path to the local data directory"
    )


# ==================================================================================================


# Read functions
# ==================================================================================================
def read_esacci_lakes_counts_of_distinct_start_days_csv(
    esacci_lakes_counts_of_distinct_start_days_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_counts_of_distinct_start_days_csv_path` into a
    :class:`pandas.DataFrame` indexed by `esacci_lakes_id`.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_csv_path : :class:`pathlib.Path`
        The path to some counts of distinct start days data csv file

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_counts_of_distinct_start_days_csv_path,
        index_col = "esacci_lakes_id"
    )


def read_esacci_lakes_hylak_fields_csv(
    esacci_lakes_hylak_fields_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_hylak_fields_csv_path` into a :class:`pandas.DataFrame`
    indexed by `esacci_lakes_id`.

    Parameters
    ----------
    esacci_lakes_hylak_fields_csv_path : :class:`pathlib.Path`
        The path to some hylak fields data csv file

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_hylak_fields_csv_path,
        index_col = "esacci_lakes_id"
    )


def read_esacci_lakes_metadata_csv(
    esacci_lakes_metadata_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_metadata_csv_path` into a :class:`pandas.DataFrame`
    indexed by `id`.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The path to the `lakescci_v2.1.0_metadata.csv` file as provided by ESA
        Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_metadata_csv_path,
        delimiter = ";",
        index_col = "id"
    )


def read_local_data_csv(
    local_data_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `local_data_csv_path` into a :class:`pandas.DataFrame` indexed by
    `esacci_lakes_id`.

    Parameters
    ----------
    local_data_csv_path : :class:`pathlib.Path`
        The path to a local data csv file

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        local_data_csv_path,
        index_col = "esacci_lakes_id"
    )


# ==================================================================================================


# System functions
# ==================================================================================================
def get_esacci_lakes_filename_time(
    path: Path
) -> datetime:
    """
    Returns the time encoded in `path`'s stem, as a :class:`datetime.datetime`.

    Parameters
    ----------
    path : :class:`pathlib.Path`
        A path named `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.*`

    Returns
    -------
    A :class:`datetime.datetime`.
    """
    date_string = path.stem.split("-")[5]

    return datetime.strptime(
        date_string,
        "%Y%m%d"
    )


# ==================================================================================================


# Validator functions
# ==================================================================================================
def argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists(
    esacci_lakes_counts_of_distinct_start_days_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_counts_of_distinct_start_days_csv_path`.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_csv_path : :class:`pathlib.Path`
        The argument `esacci_lakes_counts_of_distinct_start_days_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `esacci_lakes_counts_of_distinct_start_days_csv_path` exists.
    `False` otherwise.
    """
    if esacci_lakes_counts_of_distinct_start_days_csv_path.exists():
        return True

    if loud:
        print(
            f"error: argument esacci_lakes_counts_of_distinct_start_days_csv_path: no such file or directory: {esacci_lakes_counts_of_distinct_start_days_csv_path}",
            file = sys.stderr
        )

    return False


def argument_esacci_lakes_hylak_fields_csv_path_exists(
    esacci_lakes_hylak_fields_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_hylak_fields_csv_path`.

    Parameters
    ----------
    esacci_lakes_hylak_fields_csv_path : :class:`pathlib.Path`
        The argument `esacci_lakes_hylak_fields_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `esacci_lakes_hylak_fields_csv_path` exists. `False` otherwise.
    """
    if esacci_lakes_hylak_fields_csv_path.exists():
        return True

    if loud:
        print(
            f"error: argument esacci_lakes_hylak_fields_csv_path: no such file or directory: {esacci_lakes_hylak_fields_csv_path}",
            file = sys.stderr
        )

    return False


def argument_esacci_lakes_merged_product_dir_path_is_dir(
    esacci_lakes_merged_product_dir_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_merged_product_dir_path`.

    Parameters
    ----------
    esacci_lakes_merged_product_dir_path : :class:`pathlib.Path`
        The argument `esacci_lakes_merged_product_dir_path`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `esacci_lakes_merged_product_dir_path` is a directory. `False`
    otherwise.
    """
    if esacci_lakes_merged_product_dir_path.is_dir():
        return True

    if loud:
        print(
            f"error: argument esacci_lakes_merged_product_dir_path: not a directory: {esacci_lakes_merged_product_dir_path}",
            file = sys.stderr
        )

    return False


def argument_esacci_lakes_merged_product_nc_path_exists(
    esacci_lakes_merged_product_nc_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_merged_product_nc_path`.

    Parameters
    ----------
    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The argument `esacci_lakes_merged_product_nc_path`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `esacci_lakes_merged_product_nc_path` exists. `False` otherwise.
    """
    if esacci_lakes_merged_product_nc_path.exists():
        return True

    if loud:
        print(
            f"error: argument esacci_lakes_merged_product_nc_path: no such file or directory: {esacci_lakes_merged_product_nc_path}",
            file = sys.stderr
        )

    return False


def argument_esacci_lakes_metadata_csv_path_exists(
    esacci_lakes_metadata_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_metadata_csv_path`.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : :class:`pathlib.Path`
        The argument `esacci_lakes_metadata_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `esacci_lakes_metadata_csv_path` exists. `False` otherwise.
    """
    if esacci_lakes_metadata_csv_path.exists():
        return True

    if loud:
        print(
            f"error: argument esacci_lakes_metadata_csv_path: no such file or directory: {esacci_lakes_metadata_csv_path}",
            file = sys.stderr
        )

    return False


def argument_esacci_lakes_static_lake_mask_nc_path_exists(
    esacci_lakes_static_lake_mask_nc_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_static_lake_mask_nc_path`.

    Parameters
    ----------
    esacci_lakes_static_lake_mask_nc_path : :class:`pathlib.Path`
        The argument `esacci_lakes_static_lake_mask_nc_path`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `esacci_lakes_static_lake_mask_nc_path` exists. `False` otherwise.
    """
    if esacci_lakes_static_lake_mask_nc_path.exists():
        return True

    if loud:
        print(
            f"error: argument esacci_lakes_static_lake_mask_nc_path: no such file or directory: {esacci_lakes_static_lake_mask_nc_path}",
            file = sys.stderr
        )

    return False


def argument_esacci_lakes_variable_is_in_esacci_lakes_variables(
    esacci_lakes_variable: str,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_variable`.

    Parameters
    ----------
    esacci_lakes_variable : :class:`str`
        The argument `esacci_lakes_variable`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `esacci_lakes_variable` is in `ESACCI_LAKES_VARIABLES`. `False`
    otherwise.
    """
    if esacci_lakes_variable in ESACCI_LAKES_VARIABLES:
        return True

    if loud:
        print(
            f"error: argument esacci_lakes_variable: not in {", ".join(ESACCI_LAKES_VARIABLES)}: {esacci_lakes_variable}",
            file = sys.stderr
        )

    return False


def argument_hylak_field_is_in_hylak_fields(
    hylak_field: str,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `hylak_field`.

    Parameters
    ----------
    hylak_field : :class:`str`
        The argument `hylak_field`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `hylak_field` is in `HYLAK_FIELDS`. `False` otherwise.
    """
    if hylak_field in HYLAK_FIELDS:
        return True

    if loud:
        print(
            f"error: argument hylak_field: not in {", ".join(HYLAK_FIELDS)}: {hylak_field}",
            file = sys.stderr
        )

    return False


def argument_local_data_dir_path_is_dir(
    local_data_dir_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `local_data_dir_path`.

    Parameters
    ----------
    local_data_dir_path : :class:`pathlib.Path`
        The argument `local_data_dir_path`

    loud : :class:`bool`
        If `True`, prints an error message to stderr. default=False

    Returns
    -------
    `True` if `local_data_dir_path` is a directory. `False` otherwise.
    """
    if local_data_dir_path.is_dir():
        return True

    if loud:
        print(
            f"error: argument local_data_dir_path: not a directory: {local_data_dir_path}",
            file = sys.stderr
        )

    return False


# ==================================================================================================
