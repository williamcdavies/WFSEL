"""
Filename:   build_esa_lakes_product_csv.py
Author:     William Chuter-Davies
Modified:   03/11/26
"""

# Standard Library Imports
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )
from typing     import Any

# Related Third-party Imports
import pandas   as pd
import xarray   as xr

# Local Application/Library Specific Imports
from wfsel.exit_codes                   import (
                                            EXIT_FAILURE,
                                            EXIT_SUCCESS,
                                        )
from wfsel.io.arguments                 import add_argument_output
from wfsel.io.writers                   import to_csv
from wfsel.sources.esa_lakes.arguments  import (
                                            add_argument_esa_lakes_product_nc_path,
                                            add_argument_esa_lakes_metadata_csv_path,
                                            add_argument_esa_lakes_static_lake_mask_nc_path,
                                        )
from wfsel.sources.esa_lakes.readers    import read_esa_lakes_metadata_csv
from wfsel.utils.argparse_utils         import (
                                            arguments_are_valid as _arguments_are_valid,
                                            build_parser        as _build_parser,
                                            argument_is_file,
                                        )
from wfsel.utils.xarray_utils           import (
                                            build_geographic_bounding_box,
                                            compute_spatial_coverage,
                                            compute_spatial_mean,
                                            window,
                                        )

PROG    = "build_esa_lakes_product_csv.py"
DESC    = ""

LAKE_COVER_CLASS_WATER  = 1
LAKE_COVER_CLASS_ICE    = 2
LAKE_COVER_CLASS_CLOUD  = 3


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    """
    Wrap _build_parser.

    Returns
    -------
    ArgumentParser
        A parser
    """
    parser  = ArgumentParser(
                prog        = PROG,
                description = DESC,
                usage       = "%(prog)s [options]",
            )
    parser  = _build_parser(
                parser,
                positional_arguments    = [
                    add_argument_esa_lakes_metadata_csv_path,
                    add_argument_esa_lakes_static_lake_mask_nc_path,
                    add_argument_esa_lakes_product_nc_path,
                ],
                optional_arguments      = [
                    add_argument_output,
                ],
            )

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    """
    Wrap _arguments_are_valid.

    Parameters
    ----------
    arguments : Namespace
        The arguments

    Returns
    -------
    bool
        True if all arguments are valid, False otherwise
    """
    argument_name_to_validator  = {
                                    "esa_lakes_metadata_csv_path":          argument_is_file,
                                    "esa_lakes_static_lake_mask_nc_path":   argument_is_file,
                                    "esa_lakes_product_nc_path":            argument_is_file,
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# builder functions
# ----------------------------------------------------------------------
def build_esa_lakes_product_row(
    esa_lakes_id:                   int,
    esa_lakes_metadata_df:          pd.DataFrame,
    esa_lakes_static_lake_mask_ds:  xr.Dataset,
    esa_lakes_product_ds:           xr.Dataset,
) -> dict[str, Any]:
    """
    Build an ESA Lakes product row.

    Parameters
    ----------
    esa_lakes_id : int
        The ESA Lakes id
    esa_lakes_metadata_df : pd.DataFrame
        The ESA Lakes metadata dataframe
    esa_lakes_static_lake_mask_ds : xr.Dataset
        The ESA Lakes static lake mask dataset
    esa_lakes_product_ds : xr.Dataset
        The ESA Lakes product dataset

    Returns
    -------
    dict[str, Any]
        An ESA Lakes product row
    """
    (
        lat_max,
        lat_min,
        lon_max,
        lon_min,
    )   = esa_lakes_metadata_df.loc[
            esa_lakes_id,
            [
                "lat_max_box",
                "lat_min_box",
                "lon_max_box",
                "lon_min_box",
            ],
        ]

    bbox    = build_geographic_bounding_box(
                esa_lakes_static_lake_mask_ds,
                lat_max = lat_max,  # type: ignore[assignment]
                lat_min = lat_min,  # type: ignore[assignment]
                lon_max = lon_max,  # type: ignore[assignment]
                lon_min = lon_min,  # type: ignore[assignment]
            )

    static_lake_mask_ds_window  = window(esa_lakes_static_lake_mask_ds, bbox)
    product_ds_window           = window(esa_lakes_product_ds, bbox)

    lake_mask           = static_lake_mask_ds_window["CCI_lakeid"] == esa_lakes_id
    lake_ice_cover_mask = product_ds_window["lake_cover_class"]  == LAKE_COVER_CLASS_ICE

    x   = (
            product_ds_window["lake_surface_water_temperature"]
            .where(lake_mask)
            .where(~lake_ice_cover_mask)
        )

    observed_lake_surface_water_temperature_da      = x
    observed_lake_surface_water_temperature_mask    = x.notnull()

    lake_surface_water_temperature_mean     = compute_spatial_mean(
                                                observed_lake_surface_water_temperature_da,
                                            )
    lake_surface_water_temperature_coverage = compute_spatial_coverage(
                                                observed_lake_surface_water_temperature_mask,
                                                lake_mask,
                                            )

    row                                             = {}
    row["esa_lakes_id"]                             = esa_lakes_id
    row["lake_surface_water_temperature_mean"]      = lake_surface_water_temperature_mean
    row["lake_surface_water_temperature_coverage"]  = lake_surface_water_temperature_coverage

    return row


def build_esa_lakes_product_df(
    esa_lakes_metadata_df:          pd.DataFrame,
    esa_lakes_static_lake_mask_ds:  xr.Dataset,
    esa_lakes_product_ds:           xr.Dataset,
) -> pd.DataFrame:
    """
    Build an ESA Lakes product dataframe.

    Parameters
    ----------
    esa_lakes_metadata_df : pd.DataFrame
        The ESA Lakes metadata dataframe
    esa_lakes_static_lake_mask_ds : xr.Dataset
        The ESA Lakes static lake mask dataset
    esa_lakes_product_ds : xr.Dataset
        The ESA Lakes product dataset

    Returns
    -------
    pd.DataFrame
        An ESA Lakes product dataframe
    """
    rows    = [
                build_esa_lakes_product_row(
                    esa_lakes_id,
                    esa_lakes_metadata_df,
                    esa_lakes_static_lake_mask_ds,
                    esa_lakes_product_ds,
                )
                for esa_lakes_id
                in esa_lakes_metadata_df.index
            ]

    esa_lakes_product_df = pd.DataFrame(rows).set_index("esa_lakes_id")

    return esa_lakes_product_df


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main(
) -> int:
    """
    Run program.

    Returns
    -------
    int
        0 if program runs successfully, 1 otherwise
    """
    arguments = build_parser().parse_args()

    if not arguments_are_valid(arguments):
        return EXIT_FAILURE

    metadata_df = read_esa_lakes_metadata_csv(
                    arguments.esa_lakes_metadata_csv_path,
                )

    with (
        xr.open_dataset(arguments.esa_lakes_static_lake_mask_nc_path)   as static_lake_mask_ds,
        xr.open_dataset(arguments.esa_lakes_product_nc_path)            as product_ds,
    ):
        product_df  = build_esa_lakes_product_df(
                        metadata_df,
                        static_lake_mask_ds,
                        product_ds,
                    )

        to_csv(
            product_df,
            arguments.output,
        )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
