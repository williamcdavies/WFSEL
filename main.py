r'''
main.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib
import re
import sys

# Related Third-party Imports
import numpy  as np
import pandas as pd
import xarray as xr

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_metadata_filtered_csv_path, 
                                    add_argument_esacci_lakes_static_lake_mask_nc_path, 
                                    add_argument_esacci_lakes_merged_product_nc_path,
                                    argument_esacci_lakes_metadata_filtered_csv_path_exists, 
                                    argument_esacci_lakes_static_lake_mask_nc_path_exists, 
                                    argument_esacci_lakes_merged_product_nc_path_exists)
from lib.esacci_lakes.vars  import ESACCI_LAKES_VARIABLES
from lib.io.vars            import (RETURN_SUCCESS, 
                                    RETURN_FAILURE)


PROG = 'main.py'


def main() -> int:
   # Argument parsing
   # ==================================================================================================
   parser = argparse.ArgumentParser(prog='main.py',
                                    usage='%(prog)s [options]', 
                                    description='''Produces a .csv file containing the mean for each Lakes ECVs in `['chla', 'tsm', 'acdom440', 'Kd490', 'KdPAR', 'phycocyanin', 'lake_surface_water_temperature', 'lake_surface_water_extent']` for each lake within the candidate set given a infinite or finite buffer, ESA Lakes_cci v3.0 dataset, lakescci_v2.1_metadata.csv, and an output destination.''')

   # Positional arguments
   add_argument_esacci_lakes_metadata_filtered_csv_path(parser)
   add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
   add_argument_esacci_lakes_merged_product_nc_path(parser)
   parser.add_argument('dst_csv_path',
                       type=pathlib.Path,
                       help=f'''path to destination csv file''')
   
   args = parser.parse_args()
   # ==================================================================================================

   # Argument validation
   # ==================================================================================================
   if not argument_esacci_lakes_metadata_filtered_csv_path_exists(args.esacci_lakes_metadata_filtered_csv_path, 
                                                                  loud=True):
      return RETURN_FAILURE

   if not argument_esacci_lakes_static_lake_mask_nc_path_exists(args.esacci_lakes_static_lake_mask_nc_path, 
                                                                loud=True):
      return RETURN_FAILURE

   if not argument_esacci_lakes_merged_product_nc_path_exists(args.esacci_lakes_merged_product_nc_path, 
                                                              loud=True):
      return RETURN_FAILURE
   # ==================================================================================================
   
   # Program logic
   # ==================================================================================================
   records                   = []
   esacci_lakes_metadata_csv = pd.read_csv(args.esacci_lakes_metadata_filtered_csv_path, 
                                           delimiter=';', 
                                           index_col='id')

   with (xr.open_dataset(args.esacci_lakes_merged_product_nc_path)   as esacci_lakes_merged_product_nc, 
         xr.open_dataset(args.esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_nc):
      for row in tqdm(esacci_lakes_metadata_csv.itertuples(), 
                      total=len(esacci_lakes_metadata_csv)):
         record                        = {'id': row.Index}
         lat_max_box                   = (esacci_lakes_static_lake_mask_nc['lat'].sel(lat=row.lat_max_box, 
                                                                                      method='nearest')
                                                                                 .item())
         assert isinstance(lat_max_box, 
                           float)
         lat_min_box                   = (esacci_lakes_static_lake_mask_nc['lat'].sel(lat=row.lat_min_box, 
                                                                                      method='nearest')
                                                                                 .item())
         assert isinstance(lat_min_box, 
                           float)
         lon_max_box                   = (esacci_lakes_static_lake_mask_nc['lon'].sel(lon=row.lon_max_box, 
                                                                                      method='nearest')
                                                                                 .item())
         assert isinstance(lon_max_box, 
                           float)
         lon_min_box                   = (esacci_lakes_static_lake_mask_nc['lon'].sel(lon=row.lon_min_box, 
                                                                                      method='nearest')
                                                                                 .item())
         assert isinstance(lon_min_box, 
                           float)
         esacci_lakes_static_lake_mask = (esacci_lakes_static_lake_mask_nc['CCI_lakeid'].sel(lat=slice(lat_min_box, 
                                                                                                         lat_max_box), 
                                                                                                lon=slice(lon_min_box, 
                                                                                                         lon_max_box)) 
                                             == row.Index)
         assert isinstance(esacci_lakes_static_lake_mask, 
                           xr.DataArray)
         esacci_lakes_merged_product   = esacci_lakes_merged_product_nc.sel(lat=slice(lat_min_box, 
                                                                                      lat_max_box), 
                                                                            lon=slice(lon_min_box, 
                                                                                      lon_max_box))

         if ((esacci_lakes_merged_product[ESACCI_LAKES_VARIABLES['lake_surface_water_temperature'].var_id].where(esacci_lakes_static_lake_mask)
                                                                                                          .notnull()
                                                                                                          .sum()
                                                                                                          .item()) 
            / 
            (esacci_lakes_static_lake_mask.sum()
                                          .item())) < 0.5:
            record[f"{ESACCI_LAKES_VARIABLES['lake_surface_water_temperature'].var_id}_mean"] = np.nan
         else:
            record[f"{ESACCI_LAKES_VARIABLES['lake_surface_water_temperature'].var_id}_mean"] = (esacci_lakes_merged_product['lake_surface_water_temperature'].mean(dim=["time", "lat", "lon"], skipna=True)
                                                                                                                                                              .item())
   
         records.append(record)

   df = pd.DataFrame(records)

   df.to_csv(args.dst_csv_path, 
             index=False)

   return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())