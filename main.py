r"""
main.py

Description:
    Produces the lake surface skin temperature mean and coverage for each lake.

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from typing import Any

# Related Third-party Imports
import pandas as pd
import xarray as xr

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.geo  import (
    get_esacci_lakes_cover_class_mask,
    get_esacci_lakes_id_mask,
    get_geo_bounding_box_from_esacci_lakes_static_lake_mask
)
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_merged_product_nc_path,
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    argument_esacci_lakes_merged_product_nc_path_exists,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists,
    read_esacci_lakes_metadata_csv
)
from lib.esacci_lakes.vars       import ESACCI_LAKES_COVER_CLASS_ICE
from lib.geo.utils               import (
    get_ds_variable_coverage,
    get_ds_variable_mean,
    mask_ds,
    select_ds_by_geo_bounding_box
)
from lib.proc.utils              import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser,

    add_argument_output,
    argument_output_is_file_or_missing,
    write_df_to_csv
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)


# Constants
# ==================================================================================================
PROG = "main.py"


# ==================================================================================================


# Dataset functions
# ==================================================================================================
def get_esacci_lakes_merged_product_df(
    esacci_lakes_metadata_df:         pd.DataFrame,
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
    esacci_lakes_merged_product_ds:   xr.Dataset
) -> pd.DataFrame:
    """
    Returns a :class:`pandas.DataFrame` of each lake's lake surface skin
    temperature mean and lake surface skin temperature coverage.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    esacci_lakes_merged_product_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes merged product

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    records = [
        get_esacci_lakes_merged_product_record(
            esacci_lakes_id,
            esacci_lakes_metadata_df,
            esacci_lakes_static_lake_mask_ds,
            esacci_lakes_merged_product_ds
        )
        for esacci_lakes_id
        in esacci_lakes_metadata_df.index
    ]

    return pd.DataFrame(records).set_index("esacci_lakes_id")


def get_esacci_lakes_merged_product_record(
    esacci_lakes_id:                  int,
    esacci_lakes_metadata_df:         pd.DataFrame,
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
    esacci_lakes_merged_product_ds:   xr.Dataset
) -> dict[str, Any]:
    """
    Returns a record of `esacci_lakes_id`'s lake surface skin temperature mean
    and lake surface skin temperature coverage.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    esacci_lakes_merged_product_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes merged product

    Returns
    -------
    A :class:`dict`.
    """
    (
        lat_max_box,
        lat_min_box,
        lon_max_box,
        lon_min_box
    ) = esacci_lakes_metadata_df.loc[
        esacci_lakes_id,
        [
            "lat_max_box",
            "lat_min_box",
            "lon_max_box",
            "lon_min_box"
        ]
    ]

    geo_bounding_box = get_geo_bounding_box_from_esacci_lakes_static_lake_mask(
        esacci_lakes_static_lake_mask_ds,
        lat_max_box = lat_max_box,
        lat_min_box = lat_min_box,
        lon_max_box = lon_max_box,
        lon_min_box = lon_min_box
    )

    static_lake_mask_ds_window = select_ds_by_geo_bounding_box(
        esacci_lakes_static_lake_mask_ds,
        geo_bounding_box
    )
    merged_product_ds_window   = select_ds_by_geo_bounding_box(
        esacci_lakes_merged_product_ds,
        geo_bounding_box
    )

    id_mask  = get_esacci_lakes_id_mask(
        esacci_lakes_id,
        static_lake_mask_ds_window
    )
    ice_mask = get_esacci_lakes_cover_class_mask(
        ESACCI_LAKES_COVER_CLASS_ICE,
        merged_product_ds_window
    )

    masked_merged_product_ds_window = mask_ds(
        merged_product_ds_window[["lake_surface_water_temperature"]],
        [
            id_mask,
            ~ice_mask
        ]
    )

    record = {"esacci_lakes_id": esacci_lakes_id}
    record["lake_surface_water_temperature_mean"]     = get_ds_variable_mean(
        masked_merged_product_ds_window,
        "lake_surface_water_temperature"
    )
    record["lake_surface_water_temperature_coverage"] = get_ds_variable_coverage(
        masked_merged_product_ds_window,
        "lake_surface_water_temperature",
        id_mask
    )

    return record


# ==================================================================================================


# Parser functions
# ==================================================================================================
def build_parser(
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    return _build_parser(
        PROG,
        "Produces a .csv file containing the mean lake surface skin temperature for each lake within the candidate set.",
        positional_arguments = [
            add_argument_esacci_lakes_metadata_csv_path,
            add_argument_esacci_lakes_static_lake_mask_nc_path,
            add_argument_esacci_lakes_merged_product_nc_path
        ],
        optional_arguments   = [
            add_argument_output
        ]
    )


# ==================================================================================================


# Validator functions
# ==================================================================================================
def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Parameters
    ----------
    args : :class:`argparse.Namespace`
        The arguments

    Returns
    -------
    `True` if all arguments are successfully validated. `False` otherwise.
    """
    return _arguments_are_valid(
        args,
        [
            (
                argument_esacci_lakes_metadata_csv_path_exists,
                "esacci_lakes_metadata_csv_path"
            ),
            (
                argument_esacci_lakes_static_lake_mask_nc_path_exists,
                "esacci_lakes_static_lake_mask_nc_path"
            ),
            (
                argument_esacci_lakes_merged_product_nc_path_exists,
                "esacci_lakes_merged_product_nc_path"
            ),
            (
                argument_output_is_file_or_missing,
                "output"
            )
        ]
    )


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    metadata_df = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)

    with (
        xr.open_dataset(args.esacci_lakes_static_lake_mask_nc_path) as static_lake_mask_ds,
        xr.open_dataset(args.esacci_lakes_merged_product_nc_path)   as merged_product_ds
    ):
        merged_product_df = get_esacci_lakes_merged_product_df(
            metadata_df,
            static_lake_mask_ds,
            merged_product_ds
        )

        write_df_to_csv(
            merged_product_df,
            args.output
        )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
