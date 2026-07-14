r"""
main.py

Description: 
   The purpose of this file is to produce a .csv file containing the
   centroid mean, median, variance, maximum, and minimum values for each
   Lakes ECVs in `['chla', 'tsm', 'acdom440', 'Kd490', 'KdPAR',
   'phycocyanin', 'lake_surface_water_temperature',
   'lake_surface_water_extent']` for each lake within the candidate set
   given an ESA Lakes_cci v3.0 dataset, lakescci_v2.1_metadata.csv, and
   an output destination.

Usage:
   python main_centroid.py <lakes_cci_merg_prod_nc_path>
   <lakes_cci_meta_data_csv_path> <dst_csv_path> <buffer>

Notes:
   Only those lakes whose centroid satellite coverage exceeds 80% on a
   given day shall produce a non-NaN record.

   The buffer argument should be given in pixels. e.g., buffer=1 will
   produce a 3x3 centroid. See dataset resolution for metric sizing.

Written by William Chuter-Davies
"""


# Standard Library Imports
import pathlib
import sys
import warnings

# Related Third-party Imports
import numpy
import pandas
import tqdm
import xarray

# Local Application/Library Specific Imports
from lib.esa.vars import ECVS
from lib.io.vars  import RETURN_SUCCESS, RETURN_FAILURE


# Warning stuff
warnings.filterwarnings('ignore', category=RuntimeWarning)


def main() -> int:
   # ===================================================================================================
   # If argument count is not equal to 5, return with `RETURN_FAILURE`
   if len(sys.argv) != 5:
      print(f'fatal: unexpected argument count: {sys.argv}')
        
      return RETURN_FAILURE

   # For each path argument in `sys.argv` create corresponding
   # `pathlib.Path` and read into `paths`
   paths = [pathlib.Path(p) for p in sys.argv[1:4]]
   
   # For each path in `paths` (excluding `dst_csv_path`) ...
   for path in paths[0:2]:
      # If path does not exist, return with `RETURN_FAILURE`
      if not path.exists():
         print(f'fatal: no such file or directory: {path}')
         
         return RETURN_FAILURE

   # Read `paths` into
   # `lakes_cci_merg_prod_nc_path`,`lakes_cci_meta_data_csv_path`, and
   # `dst_csv_path`
   lakes_cci_merg_prod_nc_path, lakes_cci_meta_data_csv_path, dst_csv_path = paths

   # If buffer is not a digit string, return with `RETURN_FAILURE`
   if not sys.argv[4].isdigit():
      print(f'fatal: buffer is not a digit string: {sys.argv[4]}')
      
      return RETURN_FAILURE

   # Read buffer argument into `buffer`
   buffer = int(sys.argv[4])
   # ===================================================================================================

   # ===================================================================================================
   records = []
   
   # Attempt to ...
   try:
      # Open Dataset specified by `lakes_cci_merg_prod_nc_path`
      with xarray.open_dataset(lakes_cci_merg_prod_nc_path) as merg_prod_ds:
         # Open DataFrame specified by `lakes_cci_meta_data_csv_path`
         lakes_cci_meta_data_csv = pandas.read_csv(lakes_cci_meta_data_csv_path, delimiter=';')

         # For each row in `lakes_cci_meta_data_csv` ...
         for row in tqdm.tqdm(lakes_cci_meta_data_csv.itertuples(), total=len(lakes_cci_meta_data_csv)):
            # Read identity and boundary data into `lakes_cci_id`,
            # `lakes_cci_lat_centre`, and `lakes_cci_lon_centre`
            lakes_cci_id         = row.id
            lakes_cci_lat_centre = row.lat_centre
            lakes_cci_lon_centre = row.lon_centre
            lat_idx              = int(numpy.abs(merg_prod_ds['lat'].values - lakes_cci_lat_centre).argmin())
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
            
            # If dimensionality of centroid is not (1 + (2 * buffer)) by (1 + (2 * buffer)), continue
            if clipped_merg_prod_ds.sizes['lat'] != (1 + (2 * buffer)) or clipped_merg_prod_ds.sizes['lon'] != (1 + (2 * buffer)):
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
               
            # Read `chla` values into `reference_ecv_data`
            reference_ecv_data = clipped_merg_prod_ds['chla'].values
            
            # If the spatial coverage is less than 80%, continue
            if numpy.isnan(reference_ecv_data).sum() > (0.2 * reference_ecv_data.size):
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

            # For data variable in `ECVS`:
            for ecv in ECVS:
                # Read data variable values into `data`
                ecv_data = clipped_merg_prod_ds[ecv].values

                # Update `record` with mean, median, standard
                # deviation, variance, maximum, and minimum of `data`
                record.update({
                    f'{ecv}_mean':   numpy.nanmean(ecv_data,   axis=None).item(),
                    f'{ecv}_median': numpy.nanmedian(ecv_data, axis=None).item(),
                    f'{ecv}_var':    numpy.nanvar(ecv_data,    axis=None).item(),
                    f'{ecv}_max':    numpy.nanmax(ecv_data,    axis=None).item(),
                    f'{ecv}_min':    numpy.nanmin(ecv_data,    axis=None).item(),
                })

            records.append(record)

   # On exception, return with `RETURN_FAILURE`
   except Exception as e:
      print(f'fatal: exception: {e}')
         
      return RETURN_FAILURE
   # ===================================================================================================
   
   # ===================================================================================================
   pdf = pandas.DataFrame(records)
   pdf.to_csv(dst_csv_path, index=False)
   # =================================================================================================== 

   return RETURN_SUCCESS


if __name__ == '__main__':
   sys.exit(main())