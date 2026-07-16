r'''
main.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import pathlib
import re
import sys
import warnings

# Related Third-party Imports
import argparse
import numpy
import pandas
import tqdm
import xarray

# Local Application/Library Specific Imports
from lib.esa.vars import ECVS
from lib.io.vars  import (RETURN_SUCCESS, 
                          RETURN_FAILURE)


# Warning stuff
warnings.filterwarnings('ignore', category=RuntimeWarning)


def comp_with_inf_buffer(lakes_cci_merged_prod_nc_path: pathlib.Path,
                         lakes_cci_static_mask_nc_path: pathlib.Path, 
                         lakes_cci_meta_data_csv_path:  pathlib.Path) -> list:
   records = []

   # Open Datasets specified by `lakes_cci_merg_prod_nc_path` and
   # `lakes_cci_stat_mask_nc_path`
   with (xarray.open_dataset(lakes_cci_merged_prod_nc_path) as merg_prod_ds, 
         xarray.open_dataset(lakes_cci_static_mask_nc_path) as stat_mask_ds):
         # Open DataFrame specified by `lakes_cci_meta_data_csv_path`
         lakes_cci_meta_data_csv = pandas.read_csv(lakes_cci_meta_data_csv_path, delimiter=';')

         # For each `row` in `lakes_cci_meta_data_csv` ...
         for row in tqdm.tqdm(lakes_cci_meta_data_csv.itertuples(), total=len(lakes_cci_meta_data_csv)):
            # Read identity and boundary data into `lakes_cci_id`,
            # `lakes_cci_lat_min_box`, `lakes_cci_lat_max_box`,
            # `lakes_cci_lon_min_box`, and `lakes_cci_lon_max_box`
            lakes_cci_id          = row.id
            lakes_cci_lat_min_box = row.lat_min_box
            lakes_cci_lat_max_box = row.lat_max_box
            lakes_cci_lon_min_box = row.lon_min_box
            lakes_cci_lon_max_box = row.lon_max_box

            # Read `lakes_cci_id` into `record`
            record = {'id': lakes_cci_id}

            # Clip `merg_prod_ds` to boundary extent
            clipped_merg_prod_ds = merg_prod_ds.sel(lat=slice(lakes_cci_lat_min_box, 
                                                              lakes_cci_lat_max_box), 
                                                    lon=slice(lakes_cci_lon_min_box, 
                                                              lakes_cci_lon_max_box))
            
            # Clip `stat_mask_ds` to boundary extent
            clipped_stat_mask_ds = stat_mask_ds.sel(lat=slice(lakes_cci_lat_min_box, 
                                                              lakes_cci_lat_max_box), 
                                                    lon=slice(lakes_cci_lon_min_box, 
                                                              lakes_cci_lon_max_box))
            
            # Create geometry mask from `clipped_stat_mask_ds`
            geometry_mask = (clipped_stat_mask_ds['CCI_lakeid'].values == lakes_cci_id)

            # Read `chla` values into `reference_ecv_values`
            reference_ecv_values = clipped_merg_prod_ds['chla'].values

            # Read masked `chla` values into `reference_ecv_data`
            reference_ecv_data = reference_ecv_values[:, geometry_mask]
            
            # If geometry mask contains no `True` pixels, or complete
            # spatial coverage is less than 80%, write NaN record and
            # continue
            if (geometry_mask.sum() == 0 or 
                numpy.isnan(reference_ecv_data).sum(axis=-1)[0] > (0.2 * reference_ecv_data.shape[-1])):
               for ecv in ECVS:
                  record.update({
                     f'{ecv}_mean':   numpy.nan,
                     f'{ecv}_median': numpy.nan,
                     f'{ecv}_var':    numpy.nan,
                     f'{ecv}_max':    numpy.nan,
                     f'{ecv}_min':    numpy.nan,
                  })

               records.append(record)
               
               continue

            # For each `ecv` in `ECVS`:
            for ecv in ECVS:
               # Read ecv values into `ecv_values`
               ecv_values = clipped_merg_prod_ds[ecv].values

               # If dimensionality of `ecv_values` is not 3, continue
               if ecv_values.ndim != 3:
                  continue
               
               # Read masked ecv values into `ecv_data`
               ecv_data = ecv_values[:, geometry_mask]

               # Update `record` with mean, median, standard
               # deviation, variance, maximum, and minimum of `ecv_data`
               record.update({
                  f'{ecv}_mean':   numpy.nanmean(ecv_data,   axis=-1).item(),
                  f'{ecv}_median': numpy.nanmedian(ecv_data, axis=-1).item(),
                  f'{ecv}_var':    numpy.nanvar(ecv_data,    axis=-1).item(),
                  f'{ecv}_max':    numpy.nanmax(ecv_data,    axis=-1).item(),
                  f'{ecv}_min':    numpy.nanmin(ecv_data,    axis=-1).item(),
               })

            records.append(record)
   
   return records


def comp_with_fin_buffer(buffer:                        int, 
                         lakes_cci_merged_prod_nc_path: pathlib.Path,
                         lakes_cci_static_mask_nc_path: pathlib.Path, 
                         lakes_cci_meta_data_csv_path:  pathlib.Path) -> list:
   records = []

   # Open Datasets specified by `lakes_cci_merg_prod_nc_path` and
   # `lakes_cci_stat_mask_nc_path`
   with (xarray.open_dataset(lakes_cci_merged_prod_nc_path) as merg_prod_ds, 
         xarray.open_dataset(lakes_cci_static_mask_nc_path) as stat_mask_ds):
      # Open DataFrame specified by `lakes_cci_meta_data_csv_path`
      lakes_cci_meta_data_csv = pandas.read_csv(lakes_cci_meta_data_csv_path, delimiter=';')

      # For each `row` in `lakes_cci_meta_data_csv` ...
      for row in tqdm.tqdm(lakes_cci_meta_data_csv.itertuples(), total=len(lakes_cci_meta_data_csv)):
         # Read identity and centroid data into `lakes_cci_id`,
         # `lakes_cci_lat_centre`, `lat_idx`, `lakes_cci_lon_centre`,
         # and `lon_idx`
         lakes_cci_id         = row.id
         lakes_cci_lat_centre = row.lat_centre
         lat_idx              = int(numpy.abs(merg_prod_ds['lat'].values - lakes_cci_lat_centre).argmin())
         lakes_cci_lon_centre = row.lon_centre
         lon_idx              = int(numpy.abs(merg_prod_ds['lon'].values - lakes_cci_lon_centre).argmin())

         # Read `lakes_cci_id` into `record`
         record = {'id': lakes_cci_id}
         
         # Clip `merg_prod_ds` to centroid extent
         clipped_merg_prod_ds = merg_prod_ds.isel(lat=slice(max(lat_idx - buffer, 
                                                                0), 
                                                            lat_idx + buffer + 1), 
                                                  lon=slice(max(lon_idx - buffer, 
                                                                0), 
                                                            lon_idx + buffer + 1))
         
         clipped_stat_mask_ds = stat_mask_ds.isel(lat=slice(max(lat_idx - buffer, 
                                                                0), 
                                                            lat_idx + buffer + 1), 
                                                  lon=slice(max(lon_idx - buffer, 
                                                                0), 
                                                            lon_idx + buffer + 1))
         
         # Create geometry mask from `clipped_stat_mask_ds`
         geometry_mask = (clipped_stat_mask_ds['CCI_lakeid'].values == lakes_cci_id)

         # Read `chla` values into `reference_ecv_values`
         reference_ecv_values = clipped_merg_prod_ds['chla'].values

         # Read masked `chla` values into `reference_ecv_data`
         reference_ecv_data = reference_ecv_values[:, geometry_mask]
         
         # If `clipped_merg_prod_ds` buffer window is not (1 + (2 *
         # `buffer`)) by (1 + (2 * `buffer`)), or
         # `clipped_stat_mask_ds` buffer window is not (1 + (2 *
         # `buffer`)) by (1 + (2 * `buffer`)), or geometry mask
         # contains no `True` pixels, or centroid spatial coverage is
         # less than 80%, write NaN record and continue
         if (clipped_merg_prod_ds.sizes['lat'] != (1 + (2 * buffer)) or 
             clipped_merg_prod_ds.sizes['lon'] != (1 + (2 * buffer)) or
             clipped_stat_mask_ds.sizes['lat'] != (1 + (2 * buffer)) or
             clipped_stat_mask_ds.sizes['lon'] != (1 + (2 * buffer)) or
             geometry_mask.sum() == 0 or
             numpy.isnan(reference_ecv_data).sum(axis=-1)[0] > (0.2 * reference_ecv_data.shape[-1])):
            for ecv in ECVS:
               record.update({
                  f'{ecv}_mean':   numpy.nan,
                  f'{ecv}_median': numpy.nan,
                  f'{ecv}_var':    numpy.nan,
                  f'{ecv}_max':    numpy.nan,
                  f'{ecv}_min':    numpy.nan,
               })

            records.append(record)
            
            continue

         # For each `ecv` in `ECVS`:
         for ecv in ECVS:
            # Read ecv values into `ecv_data`
            ecv_values = clipped_merg_prod_ds[ecv].values

            # If dimensionality of `ecv_values` is not 3, continue
            if ecv_values.ndim != 3:
               continue

            # Read masked ecv values into `ecv_data`
            ecv_data = ecv_values[:, geometry_mask]

            # Update `record` with mean, median, standard
            # deviation, variance, maximum, and minimum of `ecv_data`
            record.update({
               f'{ecv}_mean':   numpy.nanmean(ecv_data,   axis=-1).item(),
               f'{ecv}_median': numpy.nanmedian(ecv_data, axis=-1).item(),
               f'{ecv}_var':    numpy.nanvar(ecv_data,    axis=-1).item(),
               f'{ecv}_max':    numpy.nanmax(ecv_data,    axis=-1).item(),
               f'{ecv}_min':    numpy.nanmin(ecv_data,    axis=-1).item(),
            })

         records.append(record)
   
   return records


def main() -> int:
   # Argument parsing
   # ==================================================================================================
   parser = argparse.ArgumentParser(prog='main.py',
                                    usage='%(prog)s [options]', 
                                    description='''Produces a .csv file
                                                containing the mean,
                                                median, variance,
                                                maximum, and minimum
                                                values for each Lakes
                                                ECVs in `['chla', 'tsm',
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
   parser.add_argument('buffer',
                        type=str,
                        help=f'''n in N | n >= 0 or 'inf''')
   parser.add_argument('lakes_cci_merged_prod_nc_path',
                       type=pathlib.Path,
                       help=f'''path to
                             `ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc`
                             as provided by ESA Lakes Climate Change
                             Initiative (Lakes_cci): Lake products,
                             Version 3.0''')
   parser.add_argument('lakes_cci_static_mask_nc_path', 
                       type=pathlib.Path, 
                       help=f'''path to `ESA_CCI_static_lake_mask.nc` as
                             provided by ESA Lakes Climate Change
                             Initiative (Lakes_cci): Lake products,
                             Version 3.0''')
   parser.add_argument('lakes_cci_meta_data_csv_path',
                       type=pathlib.Path,
                       help=f'''path to `lakescci_v2.1.0_metadata` as
                             provided by ESA Lakes Climate Change
                             Initiative (Lakes_cci): Lake products,
                             Version 3.0''')
   parser.add_argument('dst_csv_path',
                       type=pathlib.Path,
                       help=f'''path to destination csv file''')
   
   args = parser.parse_args()
   # ==================================================================================================

   # Argument validation
   # ==================================================================================================
   # If `args.buffer` is invalid, return with `RETURN_FAILURE`
   if not bool(re.fullmatch(r"^([0-9]+|inf)$", args.buffer)) :
      print(f'''error: argument buffer: unexpected value:
             {args.buffer}''')
      
      return RETURN_FAILURE
   
   # If `args.lakes_cci_merged_prod_nc_path` does not exist, return with
   # `RETURN_FAILURE`
   if not args.lakes_cci_merged_prod_nc_path.exists():
      print(f'''error: argument lakes_cci_merged_prod_nc_path: no such
             file or directory: {args.lakes_cci_merged_prod_nc_path}''')
      
      return RETURN_FAILURE

   # If `args.lakes_cci_static_mask_nc_path` does not exist, return with
   # `RETURN_FAILURE`
   if not args.lakes_cci_static_mask_nc_path.exists():
      print(f'''error: argument lakes_cci_static_mask_nc_path: no such
             file or directory: {args.lakes_cci_static_mask_nc_path}''')
      
      return RETURN_FAILURE
   
   # If `args.lakes_cci_meta_data_csv_path` does not exist, return with
   # `RETURN_FAILURE`
   if not args.lakes_cci_meta_data_csv_path.exists():
      print(f'''error: argument lakes_cci_meta_data_csv_path: no such
             file or directory: {args.lakes_cci_meta_data_csv_path}''')
      
      return RETURN_FAILURE
   # ==================================================================================================
   
   # Program logic
   # ==================================================================================================
   # Attempt to ...
   try:
      # If `args.buffer` is 'inf', run with infinite buffer
      if args.buffer == 'inf':
         records = comp_with_inf_buffer(args.lakes_cci_merged_prod_nc_path, 
                                        args.lakes_cci_static_mask_nc_path, 
                                        args.lakes_cci_meta_data_csv_path)
      # Else, run with finite buffer
      else:
         records = comp_with_fin_buffer(int(args.buffer), 
                                        args.lakes_cci_merged_prod_nc_path, 
                                        args.lakes_cci_static_mask_nc_path, 
                                        args.lakes_cci_meta_data_csv_path)
   # On exception, return with `RETURN_FAILURE`
   except Exception as e:
      print(f'error: exception: {e}')
         
      return RETURN_FAILURE
   
   # Attempt to ...
   try:
      pdf = pandas.DataFrame(records)
      pdf.to_csv(args.dst_csv_path, index=False)
   # On exception, return with `RETURN_FAILURE`
   except Exception as e:
      print(f'error: exception: {e}')
         
      return RETURN_FAILURE

   return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
   sys.exit(main())