r"""
view_chla_pcolormesh_for_one_lake.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import ArgumentParser
from pathlib  import Path

# Related Third-party Imports
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import xarray            as xr

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.argparse import (
    add_argument_esacci_lakes_id,
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    add_argument_esacci_lakes_merged_product_dir_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists,
    argument_esacci_lakes_merged_product_dir_path_exists
)
from lib.esacci_lakes.utils.geo      import get_geo_bounding_box
from lib.esacci_lakes.utils.pandas   import read_esacci_lakes_metadata_csv
from lib.geo.utils                   import sel
from lib.io.vars                     import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG = "view_chla_pcolormesh_for_one_lake.py"


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Produces a chla pcolormesh and chla_uncertainty pcolormesh visualisation for one lake"""
    )

    # Positional arguments
    add_argument_esacci_lakes_id(parser)
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
    add_argument_esacci_lakes_merged_product_dir_path(parser)

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

    if not argument_esacci_lakes_merged_product_dir_path_exists(
        args.esacci_lakes_merged_product_dir_path,
        loud=True
    ):
        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    frames_dir_path = Path(f"data/{PROG}/{args.esacci_lakes_id}/frames")
    frames_dir_path.mkdir(parents=True, exist_ok=True)

    esacci_lakes_metadata_df = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)
    esacci_lakes_metadata    = esacci_lakes_metadata_df.loc[args.esacci_lakes_id]

    with xr.open_dataset(args.esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_ds:
        geo_bounding_box = get_geo_bounding_box(
            esacci_lakes_metadata,
            esacci_lakes_static_lake_mask_ds,
        )

        esacci_lakes_static_lake_mask_ds_window = sel(
            esacci_lakes_static_lake_mask_ds,
            geo_bounding_box,
        )
        esacci_lakes_static_lake_mask           = esacci_lakes_static_lake_mask_ds_window["CCI_lakeid"] == esacci_lakes_metadata.Index
        assert isinstance(esacci_lakes_static_lake_mask, xr.DataArray)

        for i, esacci_lakes_products_merged_nc_path in enumerate(tqdm(sorted(args.esacci_lakes_merged_product_dir_path.glob("**/*.nc")))):
            with xr.open_dataset(esacci_lakes_products_merged_nc_path) as esacci_lakes_products_merged_ds:
                esacci_lakes_products_merged_ds_window = sel(
                    esacci_lakes_products_merged_ds,
                    geo_bounding_box,
                )

                esacci_lakes_nans             = esacci_lakes_products_merged_ds_window["chla"].isnull() & esacci_lakes_static_lake_mask
                esacci_lakes_vals             = esacci_lakes_products_merged_ds_window["chla"].where(esacci_lakes_static_lake_mask)
                esacci_lakes_uncertainty_nans = esacci_lakes_products_merged_ds_window["chla_uncertainty"].isnull() & esacci_lakes_static_lake_mask
                esacci_lakes_uncertainty_vals = esacci_lakes_products_merged_ds_window["chla_uncertainty"].where(esacci_lakes_static_lake_mask)

                fig, (ax1, ax2) = plt.subplots(
                    1,
                    2,
                    figsize=(12.8, 4.8)
                )

                esacci_lakes_nans.plot.pcolormesh(
                    ax=ax1,
                    vmin=0,
                    vmax=1,
                    cmap=mcolors.ListedColormap(["white", "black"]),
                    add_colorbar=False
                )
                esacci_lakes_vals.plot.pcolormesh(
                    ax=ax1,
                    norm=mcolors.LogNorm(0.01, 100),
                    cmap="viridis",
                    cbar_kwargs={"extend": "neither"}
                )

                esacci_lakes_uncertainty_nans.plot.pcolormesh(
                    ax=ax2,
                    vmin=0,
                    vmax=1,
                    cmap=mcolors.ListedColormap(["white", "black"]),
                    add_colorbar=False
                )
                esacci_lakes_uncertainty_vals.plot.pcolormesh(
                    ax=ax2,
                    vmin=0,
                    vmax=100,
                    cmap="plasma",
                    cbar_kwargs={"extend": "neither"}
                )

                frame_png_path = frames_dir_path / Path(f"frame_{i:03d}.png")
                fig.savefig(frame_png_path, dpi=300)

                plt.close(fig)

    return RETURN_SUCCESS


# ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
