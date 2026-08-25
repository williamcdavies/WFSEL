r'''
view_chla_pcolormesh_for_one_lake.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib
import sys

# Related Third-party Imports
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas            as pd
import xarray            as xr

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_id, 
                                    add_argument_esacci_lakes_metadata_csv_path, 
                                    add_argument_esacci_lakes_static_lake_mask_nc_path, 
                                    add_argument_esacci_lakes_merged_product_dir_path, 
                                    argument_esacci_lakes_metadata_csv_path_exists, 
                                    argument_esacci_lakes_static_lake_mask_nc_path_exists, 
                                    argument_esacci_lakes_merged_product_dir_path_exists)
from lib.io.vars            import (RETURN_FAILURE, 
                                    RETURN_SUCCESS)


PROG = 'view_chla_pcolormesh_for_one_lake.py'


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog=f'{PROG}',
                                     usage='%(prog)s [options]', 
                                     description='''Produces a chla pcolormesh andchla_uncertainty pcolormesh visualisation for one lake''')

    # Positional arguments
    add_argument_esacci_lakes_id(parser)
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
    add_argument_esacci_lakes_merged_product_dir_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_metadata_csv_path_exists(args.esacci_lakes_metadata_csv_path, 
                                                          loud=True):
        return RETURN_FAILURE
    
    if not argument_esacci_lakes_static_lake_mask_nc_path_exists(args.esacci_lakes_static_lake_mask_nc_path, 
                                                                 loud=True):
        return RETURN_FAILURE
    
    if not argument_esacci_lakes_merged_product_dir_path_exists(args.esacci_lakes_merged_product_dir_path, 
                                                                loud=True):
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    esacci_lakes_metadata = (pd.read_csv(args.esacci_lakes_metadata_csv_path, 
                                         delimiter=';', 
                                         index_col='id')
                               .loc[args.esacci_lakes_id])
         
    with xr.open_dataset(args.esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_nc:
        lat_max_box                   = (esacci_lakes_static_lake_mask_nc['lat'].sel(lat=esacci_lakes_metadata['lat_max_box'], 
                                                                                     method='nearest')
                                                                                .item())
        assert isinstance(lat_max_box, 
                          float)
        lat_min_box                   = (esacci_lakes_static_lake_mask_nc['lat'].sel(lat=esacci_lakes_metadata['lat_min_box'], 
                                                                                     method='nearest')
                                                                                .item())
        assert isinstance(lat_min_box, 
                          float)
        lon_max_box                   = (esacci_lakes_static_lake_mask_nc['lon'].sel(lon=esacci_lakes_metadata['lon_max_box'], 
                                                                                     method='nearest')
                                                                                .item())
        assert isinstance(lon_max_box, 
                          float)
        lon_min_box                   = (esacci_lakes_static_lake_mask_nc['lon'].sel(lon=esacci_lakes_metadata['lon_min_box'], 
                                                                                     method='nearest')
                                                                                .item())
        assert isinstance(lon_min_box, 
                          float)
        esacci_lakes_static_lake_mask = (esacci_lakes_static_lake_mask_nc['CCI_lakeid'].sel(lat=slice(lat_min_box, 
                                                                                                      lat_max_box), 
                                                                                            lon=slice(lon_min_box, 
                                                                                                      lon_max_box))
                                         == args.esacci_lakes_id)
        assert isinstance(esacci_lakes_static_lake_mask, 
                          xr.DataArray)

        frames_dir_path = pathlib.Path(f'data/{PROG}/{args.esacci_lakes_id}/frames')
        frames_dir_path.mkdir(parents=True, 
                              exist_ok=True)

        for i, esacci_lakes_products_merged_nc_path in enumerate(tqdm(sorted(args.esacci_lakes_merged_product_dir_path.glob('**/*.nc')))):
            with xr.open_dataset(esacci_lakes_products_merged_nc_path) as esacci_lakes_products_merged:
                esacci_lakes_products_merged = (esacci_lakes_products_merged[['chla', 'chla_uncertainty']].squeeze()
                                                                                                          .sel(lat=slice(lat_min_box, 
                                                                                                                         lat_max_box), 
                                                                                                               lon=slice(lon_min_box, 
                                                                                                                         lon_max_box)))
                esacci_lakes_nans               = (esacci_lakes_products_merged['chla'].isnull() 
                                                   & esacci_lakes_static_lake_mask)
                esacci_lakes_vals               = esacci_lakes_products_merged['chla'].where(esacci_lakes_static_lake_mask)
                esacci_lakes_uncertainty_nans   = (esacci_lakes_products_merged['chla_uncertainty'].isnull() 
                                                   & esacci_lakes_static_lake_mask)
                esacci_lakes_uncertainty_vals   = esacci_lakes_products_merged['chla_uncertainty'].where(esacci_lakes_static_lake_mask)

                fig, (ax1, 
                      ax2) = plt.subplots(1, 
                                          2, 
                                          figsize=(12.8, 4.8))

                esacci_lakes_nans.plot.pcolormesh(ax=ax1, 
                                                  vmin=0, 
                                                  vmax=1, 
                                                  cmap=mcolors.ListedColormap(['white', 'black']), 
                                                  add_colorbar=False)
                esacci_lakes_vals.plot.pcolormesh(ax=ax1, 
                                                  norm=mcolors.LogNorm(0.01, 100), 
                                                  cmap='viridis', 
                                                  cbar_kwargs={'extend': 'neither'})

                esacci_lakes_uncertainty_nans.plot.pcolormesh(ax=ax2, 
                                                              vmin=0, 
                                                              vmax=1, 
                                                              cmap=mcolors.ListedColormap(['white', 'black']), 
                                                              add_colorbar=False)
                esacci_lakes_uncertainty_vals.plot.pcolormesh(ax=ax2, 
                                                              vmin=0, 
                                                              vmax=100, 
                                                              cmap='plasma', 
                                                              cbar_kwargs={'extend': 'neither'})

                frame_png_path = frames_dir_path / pathlib.Path(f'frame_{i:03d}.png')
                fig.savefig(frame_png_path, dpi=300)

                plt.close(fig)

    return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())