r"""
utils.py

Description:
   Provides definitions for esacci_lakes-utility functions.

Written by William Chuter-Davies
"""

# Standard Library Imports
from argparse import ArgumentParser
from pathlib import Path

# Related Third-party Imports
import pandas as pd
import xarray as xr

# Local Application/Library Specific Imports
from lib.esacci_lakes.vars import ESACCI_LAKES_VARIABLES


# Argparse functions (main.py)
# ==================================================================================================
def add_argument_local_data_dir_path(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `local_data_dir_path` argument to a :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `local_data_dir_path` is of type :class:`Path`
    """
    parser.add_argument(
        "local_data_dir_path",
        type=Path,
        help=f"""path to the local data directory""",
    )


def argument_local_data_dir_path_exists(
    local_data_dir_path: Path,
    *,
    loud: bool = False,
) -> bool:
    """
    Returns true if `local_data_dir_path` exists, returns false
    otherwise.

    Parameters
    ----------
    local_data_dir_path : :class:`Path`
       The argument `local_data_dir_path`

    loud : bool
       If true, prints an error message to stdout. default=False
    """
    if local_data_dir_path.exists():
        return True

    if loud:
        print(
            f"""error: argument local_data_dir_path: no such file or directory: {local_data_dir_path}"""
        )

    return False


# ==================================================================================================


# Argparse functions (SQL)
# ==================================================================================================
def add_argument_esacci_lakes_average_depths_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_average_depths_csv_path` argument to a
    :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_average_depths_csv_path` is of type
    :class:`Path`
    """
    parser.add_argument(
        "esacci_lakes_average_depths_csv_path",
        type=Path,
        help=f"""path to some average depths data csv file as produced by query_esacci_lakes_average_depths.sql""",
    )


def argument_esacci_lakes_average_depths_csv_path_exists(
    esacci_lakes_average_depths_csv_path: Path,
    *,
    loud: bool = False,
) -> bool:
    """
    Returns true if `esacci_lakes_average_depths_csv_path` exists,
    returns false otherwise.

    Parameters
    ----------
    esacci_lakes_average_depths_csv_path : :class:`Path`
       The argument `esacci_lakes_average_depths_csv_path`

    loud : bool
       If true, prints an error message to stdout. default=False
    """
    if esacci_lakes_average_depths_csv_path.exists():
        return True

    if loud:
        print(
            f"""error: argument esacci_lakes_average_depths_csv_path: no such file or directory: {esacci_lakes_average_depths_csv_path}"""
        )

    return False


def add_argument_esacci_lakes_counts_of_distinct_start_days_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_counts_of_distinct_start_days_csv_path`
    argument to a :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_counts_of_distinct_start_days_csv_path` is of
    type :class:`Path`
    """
    parser.add_argument(
        "esacci_lakes_counts_of_distinct_start_days_csv_path",
        type=Path,
        help=f"""path to some counts of distinct start days data csv file as produced by query_esacci_lakes_for_counts_of_distinct_start_days.sql""",
    )


def argument_esacci_lakes_counts_of_distinct_start_days_csv_path_exists(
    esacci_lakes_counts_of_distinct_start_days_csv_path: Path,
    *,
    loud: bool = False,
) -> bool:
    """
    Returns true if
    `esacci_lakes_counts_of_distinct_start_days_csv_path` exists,
    returns false otherwise.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_csv_path : :class:`Path`
       The argument
       `esacci_lakes_counts_of_distinct_start_days_csv_path`

    loud : bool
       If true, prints an error message to stdout. default=False
    """
    if esacci_lakes_counts_of_distinct_start_days_csv_path.exists():
        return True

    if loud:
        print(
            f"""error: argument esacci_lakes_counts_of_distinct_start_days_csv_path: no such file or directory: {esacci_lakes_counts_of_distinct_start_days_csv_path}"""
        )

    return False


def add_argument_esacci_lakes_hylak_ids_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_hylak_ids_csv_path` argument to a
    :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_hylak_ids_csv_path` is of type :class:`Path`
    """
    parser.add_argument(
        "esacci_lakes_hylak_ids_csv_path",
        type=Path,
        help=f"""path to some hylaks ids data csv file as produced by query_esacci_lakes_for_hylak_ids.sql""",
    )


def argument_esacci_lakes_hylak_ids_csv_path_exists(
    esacci_lakes_hylak_ids_csv_path: Path,
    *,
    loud: bool = False,
) -> bool:
    """
    Returns true if `esacci_lakes_hylak_ids_csv_path` exists, returns
    false otherwise.

    Parameters
    ----------
    esacci_lakes_hylak_ids_csv_path : :class:`Path`
       The argument `esacci_lakes_hylak_ids_csv_path`

    loud : bool
       If true, prints an error message to stdout. default=False
    """
    if esacci_lakes_hylak_ids_csv_path.exists():
        return True

    if loud:
        print(
            f"""error: argument esacci_lakes_hylak_ids_csv_path: no such file or directory: {esacci_lakes_hylak_ids_csv_path}"""
        )

    return False


# ==================================================================================================


# Argparse functions (ESA CCI Lakes)
# ==================================================================================================
def add_argument_esacci_lakes_id(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_id` argument to a :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_id` is of type int
    """
    parser.add_argument(
        "esacci_lakes_id",
        type=int,
        help=f"""lake_cci_id as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0""",
    )


def add_argument_esacci_lakes_variable(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_variable` argument to a
    :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_variable` is of type str
    """
    parser.add_argument(
        "esacci_lakes_variable", type=str, help=f"""one of {ESACCI_LAKES_VARIABLES}"""
    )


def add_argument_esacci_lakes_metadata_csv_path(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_metadata_csv_path` argument to a
    :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_metadata_csv_path` is of type :class:`Path`
    """
    parser.add_argument(
        "esacci_lakes_metadata_csv_path",
        type=Path,
        help=f"""path to the `lakescci_v2.1.0_metadata.csv` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0""",
    )


def argument_esacci_lakes_metadata_csv_path_exists(
    esacci_lakes_metadata_csv_path: Path,
    *,
    loud: bool = False,
) -> bool:
    """
    Returns true if `esacci_lakes_metadata_csv_path` exists, returns
    false otherwise.

    Parameters
    ----------
    esacci_lakes_metadata_csv_path : :class:`Path`
       The argument `esacci_lakes_metadata_csv_path`

    loud : bool
       If true, prints an error message to stdout. default=False
    """
    if esacci_lakes_metadata_csv_path.exists():
        return True

    if loud:
        print(
            f"""error: argument esacci_lakes_metadata_csv_path: no such file or directory: {esacci_lakes_metadata_csv_path}"""
        )

    return False


def add_argument_esacci_lakes_static_lake_mask_nc_path(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_static_lake_mask_nc_path` argument to a
    :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_static_lake_mask_nc_path` is of type
    :class:`Path`
    """
    parser.add_argument(
        "esacci_lakes_static_lake_mask_nc_path",
        type=Path,
        help=f"""path to the `ESA_CCI_static_lake_mask.nc` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0""",
    )


def argument_esacci_lakes_static_lake_mask_nc_path_exists(
    esacci_lakes_static_lake_mask_nc_path: Path,
    *,
    loud: bool = False,
) -> bool:
    """
    Returns true if `esacci_lakes_static_lake_mask_nc_path` exists,
    returns false otherwise.

    Parameters
    ----------
    esacci_lakes_static_lake_mask_nc_path : :class:`Path`
       The argument `esacci_lakes_static_lake_mask_nc_path`

    loud : bool
       If true, prints an error message to stdout. default=False
    """
    if esacci_lakes_static_lake_mask_nc_path.exists():
        return True

    if loud:
        print(
            f"""error: argument esacci_lakes_static_lake_mask_nc_path: no such file or directory: {esacci_lakes_static_lake_mask_nc_path}"""
        )

    return False


def add_argument_esacci_lakes_merged_product_dir_path(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_merged_product_dir_path` argument to a
    :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_merged_product_dir_path` is of type
    :class:`Path`
    """
    parser.add_argument(
        "esacci_lakes_merged_product_dir_path",
        type=Path,
        help=f"""path to the ESA CCI merged_product directory as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0""",
    )


def argument_esacci_lakes_merged_product_dir_path_exists(
    esacci_lakes_merged_product_dir_path: Path,
    *,
    loud: bool = False,
) -> bool:
    """
    Returns true if `esacci_lakes_merged_product_dir_path` exists,
    returns false otherwise.

    Parameters
    ----------
    esacci_lakes_merged_product_dir_path : :class:`Path`
       The argument `esacci_lakes_merged_product_dir_path`

    loud : bool
       If true, prints an error message to stdout. default=False
    """
    if esacci_lakes_merged_product_dir_path.exists():
        return True

    if loud:
        print(
            f"""error: argument esacci_lakes_merged_product_dir_path: no such file or directory: {esacci_lakes_merged_product_dir_path}"""
        )

    return False


def add_argument_esacci_lakes_merged_product_nc_path(
    parser: ArgumentParser,
) -> None:
    """
    Adds an `esacci_lakes_merged_product_nc_path` argument to a
    :class:`ArgumentParser`.

    Parameters
    ----------
    parser : :class:`ArgumentParser`
       The parser

    Notes
    -----
    Argument `esacci_lakes_merged_product_nc_path` is of type
    :class:`Path`
    """
    parser.add_argument(
        "esacci_lakes_merged_product_nc_path",
        type=Path,
        help=f"""path to some `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc` file as provided by ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0""",
    )


def argument_esacci_lakes_merged_product_nc_path_exists(
    esacci_lakes_merged_product_nc_path: Path,
    *,
    loud: bool = False,
) -> bool:
    """
    Returns true if `esacci_lakes_merged_product_nc_path` exists,
    returns false otherwise.

    Parameters
    ----------
    esacci_lakes_merged_product_nc_path : :class:`Path`
       The argument `esacci_lakes_merged_product_nc_path`

    loud : bool
       If true, prints an error message to stdout. default=False
    """
    if esacci_lakes_merged_product_nc_path.exists():
        return True

    if loud:
        print(
            f"""error: argument esacci_lakes_merged_product_nc_path: no such file or directory: {esacci_lakes_merged_product_nc_path}"""
        )

    return False


# ==================================================================================================


# Geo functions
# ==================================================================================================
def bounding_box(
    esacci_lakes_id: int,
    esacci_lakes_metadata_df: pd.DataFrame,
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
) -> tuple[float, float, float, float]:
    row = esacci_lakes_metadata_df.loc[esacci_lakes_id]

    lat_max_box = (
        esacci_lakes_static_lake_mask_ds["lat"]
        .sel(lat=row.lat_max_box, method="nearest")
        .item()
    )
    assert isinstance(lat_max_box, float)
    lat_min_box = (
        esacci_lakes_static_lake_mask_ds["lat"]
        .sel(lat=row.lat_min_box, method="nearest")
        .item()
    )
    assert isinstance(lat_min_box, float)
    lon_max_box = (
        esacci_lakes_static_lake_mask_ds["lon"]
        .sel(lon=row.lon_max_box, method="nearest")
        .item()
    )
    assert isinstance(lon_max_box, float)
    lon_min_box = (
        esacci_lakes_static_lake_mask_ds["lon"]
        .sel(lon=row.lon_min_box, method="nearest")
        .item()
    )
    assert isinstance(lon_min_box, float)

    return lat_max_box, lat_min_box, lon_max_box, lon_min_box
