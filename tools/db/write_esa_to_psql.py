r'''
write_esa_to_psql.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
import pathlib
import sys

# Related Third-party Imports
import numpy
import pandas
import psycopg
import rasterio.transform
import rasterio.features
import shapely.geometry
import shapely.ops
import tqdm
import xarray

# Local Application/Library Specific Imports
from lib.io.vars import (RETURN_FAILURE, 
                         RETURN_SUCCESS)


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog='write_esa_to_psql.py',
                                     usage='%(prog)s [options]', 
                                     description='''''')

    # Positional arguments
    parser.add_argument('lakes_cci_static_mask_nc_path', 
                        type=pathlib.Path, 
                        help=f'''path to `ESA_CCI_static_lake_mask.nc`
                              as provided by ESA Lakes Climate Change
                              Initiative (Lakes_cci): Lake products,
                              Version 3.0''')
    parser.add_argument('lakes_cci_meta_data_csv_path',
                         type=pathlib.Path,
                         help=f'''path to `lakescci_v2.1.0_metadata` as
                               provided by ESA Lakes Climate Change
                               Initiative (Lakes_cci): Lake products,
                               Version 3.0''')

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    # If `args.lakes_cci_static_mask_nc_path` does not exist, return
    # with `RETURN_FAILURE`
    if not args.lakes_cci_static_mask_nc_path.exists():
        print(f'''error: argument lakes_cci_static_mask_nc_path: no
               suchfile or directory:
               {args.lakes_cci_static_mask_nc_path}''')
        
        return RETURN_FAILURE
    
    # If `args.lakes_cci_meta_data_csv_path` does not exist, return with
    # `RETURN_FAILURE`
    if not args.lakes_cci_meta_data_csv_path.exists():
        print(f'''error: argument lakes_cci_meta_data_csv_path: no such
               file or directory:
               {args.lakes_cci_meta_data_csv_path}''')
        
        return RETURN_FAILURE
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    # Open Dataset specified by `lakes_cci_merg_prod_nc_path` and
    # Database specified by `dbname=spatial`
    with (xarray.open_dataset(args.lakes_cci_static_mask_nc_path) as stat_mask_ds,
          psycopg.connect("dbname=spatial") as conn):
        # Open DataFrame specified by `lakes_cci_meta_data_csv_path`
        lakes_cci_meta_data_csv = pandas.read_csv(args.lakes_cci_meta_data_csv_path, delimiter=';')
          
        # For each `row` in `lakes_cci_meta_data_csv` ...
        for row in tqdm.tqdm(lakes_cci_meta_data_csv.itertuples(), 
                             total=len(lakes_cci_meta_data_csv)):
            # Read identity and boundary data into `lakes_cci_id`,
            # `lakes_cci_lat_min_box`, `lakes_cci_lat_max_box`,
            # `lakes_cci_lon_min_box`, and `lakes_cci_lon_max_box`
            lakes_cci_id          = row.id
            lakes_cci_lat_min_box = row.lat_min_box
            lakes_cci_lat_max_box = row.lat_max_box
            lakes_cci_lon_min_box = row.lon_min_box
            lakes_cci_lon_max_box = row.lon_max_box

            # Clip `stat_mask_ds` to boundary extent
            clipped_stat_mask_ds = stat_mask_ds.sel(lat=slice(lakes_cci_lat_min_box, 
                                                              lakes_cci_lat_max_box), 
                                                    lon=slice(lakes_cci_lon_min_box, 
                                                              lakes_cci_lon_max_box))
            
            # Create geometry mask from `clipped_stat_mask_ds`
            geometry_mask = (clipped_stat_mask_ds['CCI_lakeid'].values == lakes_cci_id)

            clipped_stat_mask_lats           = clipped_stat_mask_ds['lat'].values
            clipped_stat_mask_lons           = clipped_stat_mask_ds['lon'].values
            clipped_stat_mask_lat_resolution = float(clipped_stat_mask_lats[1] - clipped_stat_mask_lats[0])
            clipped_stat_mask_lon_resolution = float(clipped_stat_mask_lons[1] - clipped_stat_mask_lons[0])

            assert clipped_stat_mask_lon_resolution > 0

            if clipped_stat_mask_lat_resolution < 0:
                transform = rasterio.transform.from_origin(clipped_stat_mask_lons[0] - (clipped_stat_mask_lon_resolution / 2), 
                                                           clipped_stat_mask_lats[0] - (clipped_stat_mask_lat_resolution / 2), 
                                                           abs(clipped_stat_mask_lon_resolution), 
                                                           abs(clipped_stat_mask_lat_resolution))
            else:
                transform     = rasterio.transform.from_origin(clipped_stat_mask_lons[0] - (clipped_stat_mask_lon_resolution / 2), 
                                                               clipped_stat_mask_lats[-1] + (clipped_stat_mask_lat_resolution / 2), 
                                                               abs(clipped_stat_mask_lon_resolution), 
                                                               abs(clipped_stat_mask_lat_resolution))
                geometry_mask = numpy.flipud(geometry_mask)

            shapes   = rasterio.features.shapes(geometry_mask.astype(numpy.uint8), 
                                                mask=geometry_mask, 
                                                transform=transform)
            polygons = [shapely.geometry.shape(geom) for geom, _ in shapes]
            geometry = shapely.ops.unary_union(polygons)
            
            if isinstance(geometry, shapely.geometry.Polygon):
                geometry = shapely.geometry.MultiPolygon([geometry])

            wkb = shapely.to_wkb(geometry)

            with conn.cursor() as cur:
                cur.execute('''
                            INSERT INTO esa_lakes 
                                (id, 
                                 short_name, 
                                 name, 
                                 country, 
                                 max_distance_to_land, 
                                 lwl_data, 
                                 lwe_data, 
                                 lswt_data, 
                                 lic_data, 
                                 lwlr_data, 
                                 type, 
                                 geom) VALUES 
                                (%s, 
                                 %s, 
                                 %s, 
                                 %s, 
                                 %s, 
                                 %s, 
                                 %s, 
                                 %s, 
                                 %s, 
                                 %s,
                                 %s,
                                 ST_GeomFromWKB(%s, 4326))''',
                            (lakes_cci_id, 
                             row.short_name, 
                             row.name, 
                             row.country, 
                             row.max_distance_to_land, 
                             row.lwl_data,
                             row.lwe_data,
                             row.lswt_data,
                             row.lic_data,
                             row.lwlr_data,
                             row.type,
                             psycopg.Binary(wkb)))

    return RETURN_SUCCESS
   # ==================================================================================================


if __name__ == '__main__':
    sys.exit(main())