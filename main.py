r"""
main.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from typing   import Any
from pathlib  import Path

# Related Third-party Imports
import pandas as pd
import xarray as xr

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.geo import get_geo_bounding_box_from_esacci_lakes_static_lake_mask
from lib.esacci_lakes.utils.io  import (
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    add_argument_esacci_lakes_merged_product_nc_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists,
    argument_esacci_lakes_merged_product_nc_path_exists,
    read_esacci_lakes_metadata_csv
)
from lib.esacci_lakes.vars      import ESACCI_LAKES_COVER_CLASS_ICE
from lib.geo.utils              import (
    sel,
    mask
)
from lib.io.vars                import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG = "main.py"


# Argument functions
# ==================================================================================================
def build_parser(
    prog: str
) -> argparse.ArgumentParser:
    """
    Builds a :class:`ArgumentParser`.

    Parameters
    ----------
    prog : :class:`str`
        The program name

    Returns
    -------
    A :class:`ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog        = prog,
        usage       = "%(prog)s [options]",
        description = """Produces a .csv file containing the mean lake surface skin temperature for each lake within the candidate set."""
    )

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
    add_argument_esacci_lakes_merged_product_nc_path(parser)

    return parser


def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Returns
    -------
    `True` if all arguments are successfully validated. `False`
    otherwise.
    """
    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_static_lake_mask_nc_path_exists(
        args.esacci_lakes_static_lake_mask_nc_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_merged_product_nc_path_exists(
        args.esacci_lakes_merged_product_nc_path,
        loud = True
    ):
        return False

    return True


# ==================================================================================================


# Data functions
# ==================================================================================================
def get_esacci_lakes_id_mask(
    esacci_lakes_id:                  int,
    esacci_lakes_static_lake_mask_ds: xr.Dataset
) -> xr.DataArray:
    """
    Returns a boolean mask of `esacci_lakes_static_lake_mask_ds`'s
    "CCI_lakeid" pixels belonging to `esacci_lakes_id`.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The static lake mask dataset

    Returns
    -------
    A :class:`xarray.DataArray`.
    """
    return esacci_lakes_static_lake_mask_ds["CCI_lakeid"] == esacci_lakes_id


def get_esacci_lakes_cover_class_mask(
    esacci_lakes_cover_class:       int,
    esacci_lakes_merged_product_ds: xr.Dataset
) -> xr.DataArray:
    """
    Returns a boolean mask of `esacci_lakes_merged_product_ds`'s
    "lake_cover_class" pixels equal to `esacci_lakes_cover_class`.

    Parameters
    ----------
    esacci_lakes_cover_class : int
        One of `ESACCI_LAKES_COVER_CLASS_WATER`,
        `ESACCI_LAKES_COVER_CLASS_ICE`, or
        `ESACCI_LAKES_COVER_CLASS_CLOUD`

    esacci_lakes_merged_product_ds : :class:`xarray.Dataset`
        The merged product

    Returns
    -------
    A :class:`xarray.DataArray`.
    """
    return esacci_lakes_merged_product_ds["lake_cover_class"] == esacci_lakes_cover_class


def get_esacci_lakes_variable_mean(
    esacci_lakes_variable: str,
    *,
    esacci_lakes_merged_product_ds: xr.Dataset
) -> float:
    """
    Returns the mean `esacci_lakes_variable` of
    `esacci_lakes_merged_product_ds`.

    Parameters
    ----------
    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    esacci_lakes_merged_product_ds : :class:`xarray.Dataset`
        The merged product

    Returns
    -------
    A :class:`float`.
    """
    return (
        esacci_lakes_merged_product_ds[esacci_lakes_variable]
        .mean(
            dim    = ["time", "lat", "lon"],
            skipna = True
        )
        .item()
    )


def get_esacci_lakes_variable_coverage(
    esacci_lakes_variable: str,
    *,
    esacci_lakes_merged_product_ds: xr.Dataset,
    esacci_lakes_mask:              xr.DataArray
) -> float:
    """
    Returns the percentage of `esacci_lakes_mask`'s pixels with a
    non-null `esacci_lakes_variable` value in
    `esacci_lakes_merged_product_ds`.

    Parameters
    ----------
    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    esacci_lakes_merged_product_ds : :class:`xarray.Dataset`
        The merged product

    esacci_lakes_mask : :class:`xarray.DataArray`
        The base mask

    Returns
    -------
    A :class:`float`.
    """
    num = (
        esacci_lakes_merged_product_ds[esacci_lakes_variable]
        .notnull()
        .sum()
        .item()
    )
    den = (
        esacci_lakes_mask
        .sum()
        .item()
    )

    return num / den


def get_esacci_lakes_merged_product_record(
    esacci_lakes_id:                  int,
    esacci_lakes_metadata_df:         pd.DataFrame,
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
    esacci_lakes_merged_product_ds:   xr.Dataset
) -> dict[str, int | float]:
    """
    Returns a record of `esacci_lakes_id`'s lake surface skin
    temperature mean and lake surface skin temperature coverage.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id

    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    esacci_lakes_merged_product_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes merged product

    Returns
    -------
    A dict with keys "esacci_lakes_id",
    "lake_surface_water_temperature_mean", and
    "lake_surface_water_temperature_coverage".
    """
    lat_max_box: Any = esacci_lakes_metadata_df.loc[esacci_lakes_id]["lat_max_box"]
    lat_min_box: Any = esacci_lakes_metadata_df.loc[esacci_lakes_id]["lat_min_box"]
    lon_max_box: Any = esacci_lakes_metadata_df.loc[esacci_lakes_id]["lon_max_box"]
    lon_min_box: Any = esacci_lakes_metadata_df.loc[esacci_lakes_id]["lon_min_box"]

    geo_bounding_box = get_geo_bounding_box_from_esacci_lakes_static_lake_mask(
        lat_max_box,
        lat_min_box,
        lon_max_box,
        lon_min_box,
        esacci_lakes_static_lake_mask_ds
    )

    static_lake_mask_ds_window = sel(
        esacci_lakes_static_lake_mask_ds,
        geo_bounding_box
    )
    merged_product_ds_window   = sel(
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

    masked_merged_product_ds_window = mask(
        merged_product_ds_window,
        [
            id_mask,
            ~ice_mask
        ]
    )

    record: dict[str, int | float]                    = {"esacci_lakes_id": esacci_lakes_id}
    record["lake_surface_water_temperature_mean"]     = get_esacci_lakes_variable_mean(
        "lake_surface_water_temperature",
        esacci_lakes_merged_product_ds = masked_merged_product_ds_window
    )
    record["lake_surface_water_temperature_coverage"] = get_esacci_lakes_variable_coverage(
        "lake_surface_water_temperature",
        esacci_lakes_merged_product_ds = masked_merged_product_ds_window,
        esacci_lakes_mask              = id_mask
    )

    return record


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
        The :class:`pandas.DataFrame`

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    esacci_lakes_merged_product_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes merged product

    Returns
    -------
    A :class:`pandas.DataFrame` indexed by "esacci_lakes_id", with
    columns "lake_surface_water_temperature_mean" and
    "lake_surface_water_temperature_coverage".
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


def get_esacci_lakes_merged_product_fname(
    esacci_lakes_merged_product_nc_path: Path
) -> str:
    """
    Returns the output file name for
    `esacci_lakes_merged_product_nc_path`.

    Parameters
    ----------
    esacci_lakes_merged_product_nc_path : :class:`pathlib.Path`
        The path to some ESA CCI Lakes merged product netCDF file

    Returns
    -------
    A :class:`str`.
    """
    stem = esacci_lakes_merged_product_nc_path.stem
    
    return f"{stem}.csv"


# ==================================================================================================


# Write functions
# ==================================================================================================
def write_esacci_lakes_merged_product_df_to_csv(
    esacci_lakes_merged_product_df: pd.DataFrame,
    *,
    fname: str
) -> None:
    """
    Writes `esacci_lakes_merged_product_df` to `fdir / fname`.

    Parameters
    ----------
    esacci_lakes_merged_product_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`, as returned by
        `get_esacci_lakes_merged_product_df`

    fdir : :class:`pathlib.Path`
        The output file directory to write to

    fname : :class:`str`
        The output file name to write as

    Returns
    -------
    None
    """
    esacci_lakes_merged_product_df.to_csv(fname)


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()
    
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

    fname = get_esacci_lakes_merged_product_fname(args.esacci_lakes_merged_product_nc_path)

    write_esacci_lakes_merged_product_df_to_csv(
        merged_product_df,
        fname = fname
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
