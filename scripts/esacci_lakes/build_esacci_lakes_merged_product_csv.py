"""
build_esacci_lakes_merged_product_csv.py.

Written by William Chuter-Davies
"""
# Standard Library Imports
import sys

from argparse import (
    ArgumentParser,
    Namespace,
)
from typing   import Any

# Related Third-party Imports
import pandas as pd
import xarray as xr

# Local Application/Library Specific Imports
from wfsel.exit_codes                     import (
    EXIT_FAILURE,
    EXIT_SUCCESS,
)
from wfsel.io.arguments                   import add_argument_output
from wfsel.io.writers                     import to_csv
from wfsel.sources.esacci_lakes.arguments import (
    add_argument_esacci_lakes_merged_product_nc_path,
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
)
from wfsel.sources.esacci_lakes.readers   import read_esacci_lakes_metadata_csv
from wfsel.utils.argparse_utils           import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,
    argument_is_file,
)
from wfsel.utils.xarray_utils             import (
    build_geographic_bounding_box,
    compute_spatial_coverage,
    compute_spatial_mean,
    window,
)

PROG = "build_esacci_lakes_merged_product_csv.py"
DESC = ""

LAKE_COVER_CLASS_WATER = 1
LAKE_COVER_CLASS_ICE   = 2
LAKE_COVER_CLASS_CLOUD = 3


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    """
    Wrap build_parser.

    Returns
    -------
    ArgumentParser

    """
    parser = ArgumentParser(
        prog        = PROG,
        description = DESC,
        usage       = "%(prog)s [options]",
    )

    parser = _build_parser(
        parser,
        positional_arguments = [
            add_argument_esacci_lakes_metadata_csv_path,
            add_argument_esacci_lakes_static_lake_mask_nc_path,
            add_argument_esacci_lakes_merged_product_nc_path,
        ],
        optional_arguments   = [
            add_argument_output,
        ],
    )

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    """
    Wrap arguments_are_valid.

    Parameters
    ----------
    arguments : Namespace
        The arguments

    Returns
    -------
    bool

    """
    argument_name_to_validator = {
        "esacci_lakes_metadata_csv_path":        argument_is_file,
        "esacci_lakes_static_lake_mask_nc_path": argument_is_file,
        "esacci_lakes_merged_product_nc_path":   argument_is_file,
    }

    boolean = _arguments_are_valid(
        arguments,
        argument_name_to_validator,
    )

    return boolean


# ----------------------------------------------------------------------
# merged product functions
# ----------------------------------------------------------------------
def build_esacci_lakes_merged_product_df(
    esacci_lakes_metadata_df:         pd.DataFrame,
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
    esacci_lakes_merged_product_ds:   xr.Dataset,
) -> pd.DataFrame:
    """
    Build a ESA CCI Lakes merged product DataFrame.

    Parameters
    ----------
    esacci_lakes_metadata_df : pd.DataFrame
        The ESA CCI Lakes metadata
    esacci_lakes_static_lake_mask_ds : xr.Dataset
        The ESA CCI Lakes static lake mask
    esacci_lakes_merged_product_ds : xr.Dataset
        The ESA CCI Lakes merged product

    Returns
    -------
    pd.DataFrame

    """
    rows = [
        build_esacci_lakes_merged_product_row(
            esacci_lakes_id,
            esacci_lakes_metadata_df,
            esacci_lakes_static_lake_mask_ds,
            esacci_lakes_merged_product_ds,
        )
        for esacci_lakes_id
        in esacci_lakes_metadata_df.index
    ]

    esacci_lakes_merged_product_df = pd.DataFrame(rows).set_index("esacci_lakes_id")

    return esacci_lakes_merged_product_df


def build_esacci_lakes_merged_product_row(
    esacci_lakes_id:                  int,
    esacci_lakes_metadata_df:         pd.DataFrame,
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
    esacci_lakes_merged_product_ds:   xr.Dataset,
) -> dict[str, Any]:
    """
    Build a ESA CCI Lakes merged product row.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    esacci_lakes_metadata_df : pd.DataFrame
        The ESA CCI Lakes metadata
    esacci_lakes_static_lake_mask_ds : xr.Dataset
        The ESA CCI Lakes static lake mask
    esacci_lakes_merged_product_ds : xr.Dataset
        The ESA CCI Lakes merged product

    Returns
    -------
    dict[str, Any]

    """
    (
        lat_max,
        lat_min,
        lon_max,
        lon_min,
    ) = esacci_lakes_metadata_df.loc[
        esacci_lakes_id,
        [
            "lat_max_box",
            "lat_min_box",
            "lon_max_box",
            "lon_min_box",
        ],
    ]

    bbox = build_geographic_bounding_box(
        esacci_lakes_static_lake_mask_ds,
        lat_max = lat_max, # type: ignore[assignment]
        lat_min = lat_min, # type: ignore[assignment]
        lon_max = lon_max, # type: ignore[assignment]
        lon_min = lon_min, # type: ignore[assignment]
    )

    static_lake_mask_ds_window = window(
        esacci_lakes_static_lake_mask_ds,
        bbox,
    )
    merged_product_ds_window   = window(
        esacci_lakes_merged_product_ds,
        bbox,
    )

    lake_mask           = static_lake_mask_ds_window["CCI_lakeid"] == esacci_lakes_id
    lake_ice_cover_mask = merged_product_ds_window["lake_cover_class"] == LAKE_COVER_CLASS_ICE

    x = (
        merged_product_ds_window["lake_surface_water_temperature"]
        .where(lake_mask)
        .where(~lake_ice_cover_mask)
    )

    observed_lake_surface_water_temperature_da   = x
    observed_lake_surface_water_temperature_mask = x.notnull()

    lake_surface_water_temperature_mean     = compute_spatial_mean(
        observed_lake_surface_water_temperature_da,
    )
    lake_surface_water_temperature_coverage = compute_spatial_coverage(
        observed_lake_surface_water_temperature_mask,
        lake_mask,
    )

    row                                            = {}
    row["esacci_lakes_id"]                         = esacci_lakes_id
    row["lake_surface_water_temperature_mean"]     = lake_surface_water_temperature_mean
    row["lake_surface_water_temperature_coverage"] = lake_surface_water_temperature_coverage

    return row


# ----------------------------------------------------------------------
# entry point
# ----------------------------------------------------------------------
def main(
) -> int:
    """
    Entry point.

    Returns
    -------
    int

    """
    arguments = build_parser().parse_args()

    if not arguments_are_valid(arguments):
        return EXIT_FAILURE

    metadata_df = read_esacci_lakes_metadata_csv(arguments.esacci_lakes_metadata_csv_path)

    with (
        xr.open_dataset(arguments.esacci_lakes_static_lake_mask_nc_path) as static_lake_mask_ds,
        xr.open_dataset(arguments.esacci_lakes_merged_product_nc_path)   as merged_product_ds,
    ):
        merged_product_df = build_esacci_lakes_merged_product_df(
            metadata_df,
            static_lake_mask_ds,
            merged_product_ds,
        )

        to_csv(
            merged_product_df,
            arguments.output,
        )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
