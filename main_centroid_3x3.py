r"""
main.py

Description: 
   The purpose of this file is to produce a .csv file containing the 3x3
   centroid value for each Lakes ECVs in `['chla', 'tsm', 'acdom440',
   'Kd490', 'KdPAR', 'phycocyanin', 'lake_surface_water_temperature',
   'lake_surface_water_extent']` for each lake within the candidate set
   given an ESA Lakes_cci v3.0 dataset, lakescci_v2.1_metadata.csv, and
   an output destination.


Usage:
   python main_centroid.py <lakes_cci_merg_prod_nc_path> <csv_path>
   <dst_path>

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
    # If argument count is not equal to 4, return with `RETURN_FAILURE`
    if len(sys.argv) != 4:
        print(f'fatal: unexpected argument count: {sys.argv}')
            
        return RETURN_FAILURE

    # For each path in `sys.argv` create corresponding Path and read into
    # `paths`
    paths = [pathlib.Path(p) for p in sys.argv[1:4]]
    
    # For each path in `paths` (excluding `dst_path`) ...
    for path in paths[0:2]:
        # If path does not exist, return with `RETURN_FAILURE`
        if not path.exists():
            print(f'fatal: no such file or directory: {path}')
            
            return RETURN_FAILURE

    # Read `paths` into `lakes_cci_merg_prod_nc_path`, `csv_path`, and
    # `dst_path`
    lakes_cci_merg_prod_nc_path, csv_path, dst_path = paths

    records = []
   
    # Attempt to ...
    try:
        # Open Datasets specified by `lakes_cci_merg_prod_nc_path`
        with xarray.open_dataset(lakes_cci_merg_prod_nc_path) as merg_prod_ds:
            # Open DataFrame specified by `csv_path`
            csv = pandas.read_csv(csv_path, delimiter=';')

            # For each row in `csv` ...
            for row in tqdm.tqdm(csv.itertuples(), total=len(csv)):
                # Read identity and boundary data into `lakes_cci_id`,
                # `lakes_cci_lat_centre`, and `lakes_cci_lon_centre`
                lakes_cci_id         = row.id
                lakes_cci_lat_centre = row.lat_centre
                lakes_cci_lon_centre = row.lon_centre

                lat_idx   = int(numpy.abs(merg_prod_ds['lat'].values - lakes_cci_lat_centre).argmin())
                lon_idx   = int(numpy.abs(merg_prod_ds['lon'].values - lakes_cci_lon_centre).argmin())
                
                clipped_merg_prod_ds = merg_prod_ds.isel(lat=slice(max(lat_idx - 1, 
                                                                      0), 
                                                                   lat_idx + 2), 
                                                         lon=slice(max(lon_idx - 1, 
                                                                      0), 
                                                                   lon_idx + 2))

                # Read `lakes_cci_id` into `record`
                record = {'id': lakes_cci_id}

                # Read `chla` values into `reference_data`
                reference_data = clipped_merg_prod_ds['chla'].values
                
                # If the spatial coverage is less than 80%, continue
                if numpy.isnan(reference_data).sum() > (0.2 * reference_data.size):
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

                # For data variable in `DATA_VARS`:
                for data_var in DATA_VARS:
                    # Read data variable values into `data`
                    data = clipped_merg_prod_ds[data_var].values

                    # Update `record` with mean, median, standard
                    # deviation, variance, maximum, and minimum of `data`
                    record.update({
                        f'{data_var}_mean':   numpy.nanmean(data, ).item(),
                        f'{data_var}_median': numpy.nanmedian(data).item(),
                        f'{data_var}_var':    numpy.nanstd(data,  ).item(),
                        f'{data_var}_max':    numpy.nanmax(data,  ).item(),
                        f'{data_var}_min':    numpy.nanmin(data,  ).item(),
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