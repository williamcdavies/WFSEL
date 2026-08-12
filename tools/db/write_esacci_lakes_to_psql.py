r'''
write_esacci_lakes_to_psql.py

Written by William Chuter-Davies
'''


# Standard Library Imports
import argparse
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
from lib.io.vars            import (RETURN_FAILURE, 
                                    RETURN_SUCCESS)
from lib.esacci_lakes.utils import (add_argument_esacci_lakes_metadata_csv_path, 
                                    add_argument_esacci_lakes_static_lake_mask_nc_path, 
                                    argument_esacci_lakes_metadata_csv_path_exists, 
                                    argument_esacci_lakes_static_lake_mask_nc_path_exists)


PROG='write_esacci_lakes_to_psql.py'


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = argparse.ArgumentParser(prog=f'{PROG}.py',
                                     usage='%(prog)s [options]', 
                                     description='''Writes ESA Lakes
                                                 Climate Change
                                                 Initiative (Lakes_cci):
                                                 Lake products, Version
                                                 3.0 metadata and
                                                 geometries to psql for
                                                 use with PostGIS.''')

    # Positional arguments
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
    add_argument_esacci_lakes_metadata_csv_path(parser)

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
    # ==================================================================================================
    
    # Program logic
    # ==================================================================================================
    esacci_lakes_metadata_csv = pandas.read_csv(args.esacci_lakes_metadata_csv_path, 
                                                delimiter=';', 
                                                index_col='id')
    
    with (xarray.open_dataset(args.esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_nc,
          psycopg.connect("dbname=spatial")                               as conn):
        for row in tqdm.tqdm(esacci_lakes_metadata_csv.itertuples(), 
                             total=len(esacci_lakes_metadata_csv)):
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

            lons = esacci_lakes_static_lake_mask['lon'].values
            lats = esacci_lakes_static_lake_mask['lat'].values

            transform = rasterio.transform.from_bounds(lons.min(), 
                                                       lats.min(), 
                                                       lons.max(), 
                                                       lats.max(), 
                                                       len(lons), 
                                                       len(lats))
            mask     = numpy.flipud(esacci_lakes_static_lake_mask.values)
            shapes   = rasterio.features.shapes(mask.astype(numpy.uint8), 
                                                mask=mask, 
                                                transform=transform)
            polygons = [shapely.geometry.shape(geom) for geom, _ in shapes]
            geometry = shapely.ops.unary_union(polygons)

            if isinstance(geometry, shapely.geometry.Polygon):
                geometry = shapely.geometry.MultiPolygon([geometry])

            wkb = shapely.to_wkb(geometry)

            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO esacci_lakes 
                        (id, 
                        short_name, 
                        name, 
                        country, 
                        max_distance_to_land, 
                        lat_min_box, 
                        lat_max_box, 
                        lon_min_box, 
                        lon_max_box, 
                        lat_centre, 
                        lon_centre, 
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
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                     ST_GeomFromWKB(%s, 4326))''',
                (row.Index, 
                 row.short_name, 
                 row.name, 
                 row.country, 
                 row.max_distance_to_land, 
                 row.lat_min_box, 
                 row.lat_max_box, 
                 row.lon_min_box, 
                 row.lon_max_box, 
                 row.lat_centre, 
                 row.lon_centre, 
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