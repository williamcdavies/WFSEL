r"""
main.py

Description: 
   The purpose of this file is to produce a .csv file containing mean,
   median, variance, maximum, and minimum values for each Lakes ECVs in
   `['chla', 'tsm', 'acdom440', 'Kd490', 'KdPAR', 'phycocyanin',
   'lake_surface_water_temperature', 'lake_surface_water_extent']` for
   each lake within the candidate set given an ESA Lakes_cci v3.0
   dataset, ESA_CCI_static_lake_mask.nc, lakescci_v2.1_metadata.csv, and
   an output destination.


Usage:
   python main.py <lakes_cci_merg_prod_nc_path>
   <lakes_cci_stat_mask_nc_path> <csv_path> <dst_path>

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


# Warning stuff
warnings.filterwarnings('ignore', category=RuntimeWarning)


# Global Definitions
RETURN_SUCCESS = 0
RETURN_FAILURE = 1
DATA_VARS = ['chla', 
             'tsm', 
             'acdom440', 
             'Kd490', 
             'KdPAR',
             'phycocyanin', 
             'lake_surface_water_temperature',
             'lake_surface_water_extent']


def main() -> int:
   # If argument count is not equal to 5, return with `RETURN_FAILURE`
   if len(sys.argv) != 5:
      print(f'fatal: unexpected argument count: {sys.argv}')
        
      return RETURN_FAILURE

   # For each path in `sys.argv` create corresponding Path and read into
   # `paths`
   paths = [pathlib.Path(p) for p in sys.argv[1:5]]
   
   # For each path in `paths` (excluding `dst_path`) ...
   for path in paths[0:3]:
      # If path does not exist, return with `RETURN_FAILURE`
      if not path.exists():
         print(f'fatal: no such file or directory: {path}')
         
         return RETURN_FAILURE

   # Read `paths` into `lakes_cci_merg_prod_nc_path`,
   # `lakes_cci_stat_mask_nc_path`, `csv_path`, and `dst_path`
   lakes_cci_merg_prod_nc_path, lakes_cci_stat_mask_nc_path, csv_path, dst_path = paths

   records = []
   
   # Attempt to ...
   try:
      # Open Datasets specified by `lakes_cci_merg_prod_nc_path` and
      # `lakes_cci_stat_mask_nc_path`
      with xarray.open_dataset(lakes_cci_merg_prod_nc_path) as merg_prod_ds, xarray.open_dataset(lakes_cci_stat_mask_nc_path) as stat_mask_ds:
         # Open DataFrame specified by `csv_path`
         csv = pandas.read_csv(csv_path, delimiter=';')

         # For each row in `csv` ...
         for row in tqdm.tqdm(csv.itertuples(), total=len(csv)):
            # Read identity and boundary data into `lakes_cci_id`,
            # `lakes_cci_lat_min_box`, `lakes_cci_lat_max_box`,
            # `lakes_cci_lon_min_box`, and `lakes_cci_lon_max_box`
            lakes_cci_id          = row.id
            lakes_cci_lat_min_box = row.lat_min_box
            lakes_cci_lat_max_box = row.lat_max_box
            lakes_cci_lon_min_box = row.lon_min_box
            lakes_cci_lon_max_box = row.lon_max_box

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

            # Read `lakes_cci_id` into `record`
            record = {'id': lakes_cci_id}

            # Read `chla` values into `reference_data_var_values`
            reference_data_var_values = clipped_merg_prod_ds['chla'].values

            # Read masked `chla` values into `referenc_data`
            reference_data            = reference_data_var_values[:, geometry_mask]
            
            # If the spatial coverage is less than 80%, continue
            if numpy.isnan(reference_data).sum(axis=-1)[0] > (0.2 * reference_data.shape[-1]):
                  for data_var in DATA_VARS:
                     record.update({
                        f'{data_var}_mean':   numpy.nan,
                        f'{data_var}_median': numpy.nan,
                        f'{data_var}_var':    numpy.nan,
                        f'{data_var}_max':    numpy.nan,
                        f'{data_var}_min':    numpy.nan,
                     })

                  records.append(record)
                  continue

            # For each data variable in `clipped_merg_prod_ds.data_vars` ...
            # for data_var in clipped_merg_prod_ds.data_vars:
            for data_var in DATA_VARS:
               # Read data variable values into `data_var_values`
               data_var_values = clipped_merg_prod_ds[data_var].values

               # If dimensionality of `data_var_values` is not 3, continue
               if data_var_values.ndim != 3:
                  continue
               
               # Read masked data variable values into `data`
               data = data_var_values[:, geometry_mask]

               # Update `record` with mean, median, standard
               # deviation, variance, maximum, and minimum of `data`
               record.update({
                  f'{data_var}_mean':   numpy.nanmean(data,   axis=-1).item(),
                  f'{data_var}_median': numpy.nanmedian(data, axis=-1).item(),
                  f'{data_var}_var':    numpy.nanstd(data,    axis=-1).item(),
                  f'{data_var}_max':    numpy.nanmax(data,    axis=-1).item(),
                  f'{data_var}_min':    numpy.nanmin(data,    axis=-1).item(),
               })

            records.append(record)

   # On exception, return with `RETURN_FAILURE`
   except Exception as e:
      print(f'fatal: exception: {e}')
         
      return RETURN_FAILURE
   
   pdf = pandas.DataFrame(records)
   pdf.to_csv(dst_path, index=False)
       
   return RETURN_SUCCESS


if __name__ == '__main__':
    sys.exit(main())