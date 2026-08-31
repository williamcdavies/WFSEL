r"""
main.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import ArgumentParser
from pathlib  import Path

# Related Third-party Imports
import numpy  as np
import pandas as pd
import xarray as xr

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.argparse import (
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    add_argument_esacci_lakes_merged_product_nc_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists,
    argument_esacci_lakes_merged_product_nc_path_exists
)
from lib.esacci_lakes.utils.geo      import get_geo_bounding_box
from lib.esacci_lakes.utils.pandas   import read_esacci_lakes_metadata_csv
from lib.esacci_lakes.vars           import ESACCI_LAKES_VARIABLES
from lib.geo.utils                   import sel
from lib.io.vars                     import (
    RETURN_SUCCESS,
    RETURN_FAILURE
)

PROG = "main.py"


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Produces a .csv file containing the mean for each Lakes ECVs in `['chla', 'tsm', 'acdom440', 'Kd490', 'KdPAR', 'phycocyanin', 'lake_surface_water_temperature', 'lake_surface_water_extent']` for each lake within the candidate set given a infinite buffer, ESA Lakes_cci v3.0 dataset, lakescci_v2.1_metadata.csv, and an output destination."""
    )

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
    add_argument_esacci_lakes_merged_product_nc_path(parser)
    parser.add_argument(
        "output_csv_path",
        type=Path,
        help=f"""path to output csv file"""
    )

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path,
        loud=True
    ):
        return RETURN_FAILURE

    if not argument_esacci_lakes_static_lake_mask_nc_path_exists(
        args.esacci_lakes_static_lake_mask_nc_path,
        loud=True
    ):
        return RETURN_FAILURE

    if not argument_esacci_lakes_merged_product_nc_path_exists(
        args.esacci_lakes_merged_product_nc_path,
        loud=True
    ):
        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    records = []

    esacci_lakes_metadata_df = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)

    with (
        xr.open_dataset(args.esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_ds,
        xr.open_dataset(args.esacci_lakes_merged_product_nc_path)   as esacci_lakes_merged_product_ds
    ):
        for row in tqdm(
            esacci_lakes_metadata_df.itertuples(),
            total=len(esacci_lakes_metadata_df)
        ):
            record = {"esacci_lakes_id": row.Index}

            geo_bounding_box = get_geo_bounding_box(
                row,
                esacci_lakes_static_lake_mask_ds
            )

            esacci_lakes_static_lake_mask_ds_window = sel(
                esacci_lakes_static_lake_mask_ds,
                geo_bounding_box
            )
            esacci_lakes_static_lake_mask_a         = esacci_lakes_static_lake_mask_ds_window["CCI_lakeid"] == row.Index
            assert isinstance(esacci_lakes_static_lake_mask_a, xr.DataArray)

            esacci_lakes_merged_product_ds_window   = sel(
                esacci_lakes_merged_product_ds,
                geo_bounding_box
            )
            esacci_lakes_static_lake_mask_b         = esacci_lakes_merged_product_ds_window["lake_surface_water_temperature"] >= 277.15
            assert isinstance(esacci_lakes_static_lake_mask_b, xr.DataArray)

            for esacci_lakes_variable in ESACCI_LAKES_VARIABLES:
                record[f"{esacci_lakes_variable}_mean"] = (
                    esacci_lakes_merged_product_ds_window[esacci_lakes_variable]
                    .where(esacci_lakes_static_lake_mask_a)
                    .where(esacci_lakes_static_lake_mask_b)
                    .mean(
                        dim=[
                            "time",
                            "lat",
                            "lon"
                        ],
                        skipna=True
                    )
                    .item()
                )

            numer = (
                (esacci_lakes_static_lake_mask_a & esacci_lakes_static_lake_mask_b)
                .sum()
                .item()
            )
            denom = (
                esacci_lakes_static_lake_mask_a
                .sum()
                .item()
            )

            record["coverage"] = 100 * (numer / denom) if denom > 0 else np.nan
            records.append(record)

    output_df = pd.DataFrame(records)
    output_df.to_csv(
        args.output_csv_path,
        index=False
    )

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
