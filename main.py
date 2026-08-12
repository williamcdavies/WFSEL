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
import numpy
import pandas
import tqdm
import xarray

# Local Application/Library Specific Imports
from lib.io.vars            import (RETURN_SUCCESS, 
                                    RETURN_FAILURE)
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_metadata_csv_path, 
                                    add_argument_esacci_lakes_products_merged_nc_path,
                                    add_argument_esacci_lakes_static_lake_mask_nc_path, 
                                    argument_esacci_lakes_metadata_csv_path_exists, 
                                    argument_esacci_lakes_products_merged_nc_path_exists, 
                                    argument_esacci_lakes_static_lake_mask_nc_path_exists)
from lib.esacci_lakes.vars  import ESACCI_LAKES_VARIABLES


PROG = 'main.py'


def comp_with_inf_buffer(esacci_lakes_metadata_csv_path:        pathlib.Path,
                         esacci_lakes_products_merged_nc_path:  pathlib.Path,
                         esacci_lakes_static_lake_mask_nc_path: pathlib.Path) -> list:
   records                   = []
   esacci_lakes_metadata_csv = pandas.read_csv(esacci_lakes_metadata_csv_path, 
                                               delimiter=';', 
                                               index_col='id')

   with (xarray.open_dataset(esacci_lakes_products_merged_nc_path)  as esacci_lakes_products_merged_nc, 
         xarray.open_dataset(esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_nc):
         for row in tqdm.tqdm(esacci_lakes_metadata_csv.itertuples(), 
                              total=len(esacci_lakes_metadata_csv)):
            record                          = {'id': row.Index}
            lat_max_box                     = (esacci_lakes_static_lake_mask_nc['lat'].sel(lat=row.lat_max_box, 
                                                                                           method='nearest')
                                                                                      .item())
            assert isinstance(lat_max_box, 
                              float)
            lat_min_box                     = (esacci_lakes_static_lake_mask_nc['lat'].sel(lat=row.lat_min_box, 
                                                                                           method='nearest')
                                                                                      .item())
            assert isinstance(lat_min_box, 
                              float)
            lon_max_box                     = (esacci_lakes_static_lake_mask_nc['lon'].sel(lon=row.lon_max_box, 
                                                                                           method='nearest')
                                                                                      .item())
            assert isinstance(lon_max_box, 
                              float)
            lon_min_box                     = (esacci_lakes_static_lake_mask_nc['lon'].sel(lon=row.lon_min_box, 
                                                                                           method='nearest')
                                                                                      .item())
            assert isinstance(lon_min_box, 
                              float)
            esacci_lakes_static_lake_mask   = (esacci_lakes_static_lake_mask_nc.sel(lat=slice(lat_min_box, 
                                                                                              lat_max_box), 
                                                                                    lon=slice(lon_min_box, 
                                                                                              lon_max_box))['CCI_lakeid']
                                               == row.Index)
            assert isinstance(esacci_lakes_static_lake_mask, 
                              xarray.DataArray)
            esacci_lakes_products_merged    = esacci_lakes_products_merged_nc.sel(lat=slice(lat_min_box, 
                                                                                            lat_max_box), 
                                                                                  lon=slice(lon_min_box, 
                                                                                            lon_max_box))

            for esacci_lakes_variable in ESACCI_LAKES_VARIABLES:
               if ((esacci_lakes_products_merged[esacci_lakes_variable.var_id].where(esacci_lakes_static_lake_mask)
                                                                              .notnull()
                                                                              .sum()
                                                                              .item()) 
                   / (esacci_lakes_static_lake_mask.sum()
                                                   .item())) < 0.8:
                  record.update({f'{esacci_lakes_variable.var_id}_mean': numpy.nan})
               else:
                  record.update({f'{esacci_lakes_variable.var_id}_mean': numpy.nanmean(esacci_lakes_products_merged[esacci_lakes_variable.var_id].where(esacci_lakes_static_lake_mask)
                                                                                                                                                 .values)})

            records.append(record)
   
   return records


def comp_with_fin_buffer(buffer:                                int, 
                         esacci_lakes_metadata_csv_path:        pathlib.Path,
                         esacci_lakes_products_merged_nc_path:  pathlib.Path,
                         esacci_lakes_static_lake_mask_nc_path: pathlib.Path) -> list:
   records                   = []
   esacci_lakes_metadata_csv = pandas.read_csv(esacci_lakes_metadata_csv_path, 
                                               delimiter=';', 
                                               index_col='id')

   with (xarray.open_dataset(esacci_lakes_products_merged_nc_path)  as esacci_lakes_products_merged_nc, 
         xarray.open_dataset(esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_nc):
         for row in tqdm.tqdm(esacci_lakes_metadata_csv.itertuples(), 
                              total=len(esacci_lakes_metadata_csv)):
            record                          = {'id': row.Index}
            lat_centre                      = (esacci_lakes_static_lake_mask_nc['lat'].sel(lat=row.lat_centre, 
                                                                                           method='nearest')
                                                                                      .item())
            assert isinstance(lat_centre, 
                              float)
            lat_centre_idx                  = (esacci_lakes_static_lake_mask_nc['lat'].get_index('lat')
                                                                                      .get_loc(lat_centre))
            assert isinstance(lat_centre_idx, 
                              int)
            lon_centre                      = (esacci_lakes_static_lake_mask_nc['lon'].sel(lon=row.lon_centre, 
                                                                                           method='nearest')
                                                                                      .item())
            assert isinstance(lon_centre, 
                              float)
            lon_centre_idx                  = (esacci_lakes_static_lake_mask_nc['lon'].get_index('lon')
                                                                                      .get_loc(lon_centre))
            assert isinstance(lon_centre_idx, 
                              int)
            esacci_lakes_static_lake_mask   = (esacci_lakes_static_lake_mask_nc.isel(lat=slice(max(lat_centre_idx - buffer, 
                                                                                                   0), 
                                                                                               lat_centre_idx + buffer + 1), 
                                                                                     lon=slice(max(lon_centre_idx - buffer, 
                                                                                                   0), 
                                                                                               lon_centre_idx + buffer + 1))['CCI_lakeid'] 
                                               == row.Index)
            assert isinstance(esacci_lakes_static_lake_mask, 
                              xarray.DataArray)
            esacci_lakes_products_merged = esacci_lakes_products_merged_nc.isel(lat=slice(max(lat_centre_idx - buffer, 
                                                                                              0), 
                                                                                          lat_centre_idx + buffer + 1), 
                                                                                lon=slice(max(lon_centre_idx - buffer, 
                                                                                              0), 
                                                                                          lon_centre_idx + buffer + 1))

            for esacci_lakes_variable in ESACCI_LAKES_VARIABLES:
               if ((esacci_lakes_products_merged[esacci_lakes_variable.var_id].where(esacci_lakes_static_lake_mask)
                                                                              .notnull()
                                                                              .sum()
                                                                              .item()) 
                     / (esacci_lakes_static_lake_mask.sum()
                                                     .item())) < 0.8:
                  record.update({f'{esacci_lakes_variable.var_id}_mean': numpy.nan})
               else:
                  record.update({f'{esacci_lakes_variable.var_id}_mean': numpy.nanmean(esacci_lakes_products_merged[esacci_lakes_variable.var_id].where(esacci_lakes_static_lake_mask)
                                                                                                                                                 .values)})

            records.append(record)
   
   return records


def main() -> int:
   # Argument parsing
   # ==================================================================================================
   parser = argparse.ArgumentParser(prog='main.py',
                                    usage='%(prog)s [options]', 
                                    description='''Produces a .csv file
                                                containing the mean for
                                                each Lakes ECVs in
                                                `['chla', 'tsm',
                                                'acdom440', 'Kd490',
                                                'KdPAR', 'phycocyanin',
                                                'lake_surface_water_temperature',
                                                'lake_surface_water_extent']`
                                                for each lake within the
                                                candidate set given a
                                                infinite or finite
                                                buffer, ESA Lakes_cci
                                                v3.0 dataset,
                                                lakescci_v2.1_metadata.csv,
                                                and an output
                                                destination.''')

   # Positional arguments
   add_argument_esacci_lakes_metadata_csv_path(parser)
   add_argument_esacci_lakes_products_merged_nc_path(parser)
   add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
   parser.add_argument('buffer',
                        type=str,
                        help=f'''n in N | n >= 0 or "inf"''')
   parser.add_argument('dst_csv_path',
                       type=pathlib.Path,
                       help=f'''path to destination csv file''')
   
   args = parser.parse_args()
   # ==================================================================================================

   # Argument validation
   # ==================================================================================================
   if not argument_esacci_lakes_metadata_csv_path_exists(args.esacci_lakes_metadata_csv_path, 
                                                        loud=True):
      return RETURN_FAILURE

   if not argument_esacci_lakes_products_merged_nc_path_exists(args.esacci_lakes_products_merged_nc_path, 
                                                               loud=True):
      return RETURN_FAILURE

   if not argument_esacci_lakes_static_lake_mask_nc_path_exists(args.esacci_lakes_static_lake_mask_nc_path, 
                                                                loud=True):
      return RETURN_FAILURE

   if not bool(re.fullmatch(r"^([0-9]+|inf)$", 
                            args.buffer)) :
      print(f'''error: argument buffer: unexpected value:
             {args.buffer}''')
      
      return RETURN_FAILURE
   # ==================================================================================================
   
   # Program logic
   # ==================================================================================================
   try:
      if args.buffer == 'inf':
         records = comp_with_inf_buffer(args.esacci_lakes_metadata_csv_path, 
                                        args.esacci_lakes_products_merged_nc_path, 
                                        args.esacci_lakes_static_lake_mask_nc_path)
      else:
         records = comp_with_fin_buffer(int(args.buffer), 
                                        args.esacci_lakes_metadata_csv_path, 
                                        args.esacci_lakes_products_merged_nc_path, 
                                        args.esacci_lakes_static_lake_mask_nc_path)
   except Exception as e:
      print(f'error: exception: {e}')
         
      return RETURN_FAILURE
   
   try:
      df = pandas.DataFrame(records)

      df.to_csv(args.dst_csv_path, 
                index=False)
   except Exception as e:
      print(f'error: exception: {e}')
         
      return RETURN_FAILURE

   return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())