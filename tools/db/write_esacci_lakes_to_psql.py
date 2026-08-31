r"""
write_esacci_lakes_to_psql.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import ArgumentParser

# Related Third-party Imports
import numpy              as np
import psycopg
import psycopg.sql
import rasterio.features
import rasterio.transform
import shapely.ops
import xarray             as xr

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.argparse import (
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists
)
from lib.esacci_lakes.utils.geo      import get_geo_bounding_box
from lib.esacci_lakes.utils.pandas   import read_esacci_lakes_metadata_csv
from lib.geo.utils                   import sel
from lib.io.vars                     import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG = "write_esacci_lakes_to_psql.py"


def to_wkb(
    esacci_lakes_static_lake_mask: xr.DataArray,
) -> bytes:
    lons = esacci_lakes_static_lake_mask["lon"].values
    lats = esacci_lakes_static_lake_mask["lat"].values

    mask      = np.flipud(esacci_lakes_static_lake_mask.values)
    transform = rasterio.transform.from_bounds(
        west=lons.min(),
        south=lats.min(),
        east=lons.max(),
        north=lats.max(),
        width=len(lons),
        height=len(lats)
    )

    shapes = rasterio.features.shapes(
        mask.astype(np.uint8),
        mask=mask,
        transform=transform
    )

    geometry = shapely.ops.unary_union([shapely.geometry.shape(polygon) for polygon, _ in shapes])

    if isinstance(geometry, shapely.geometry.Polygon):
        geometry = shapely.geometry.MultiPolygon([geometry])

    return shapely.to_wkb(geometry)


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description="""Writes ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0 metadata and geometries to psql for use with PostGIS.""",
    )

    # Positional arguments
    add_argument_esacci_lakes_metadata_csv_path(parser)
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)

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
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    esacci_lakes_metadata_df = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)

    with (
        xr.open_dataset(args.esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_ds,
        psycopg.connect("dbname=spatial") as conn
    ):
        for row in tqdm(
            esacci_lakes_metadata_df.itertuples(),
            total=len(esacci_lakes_metadata_df)
        ):
            geo_bounding_box                        = get_geo_bounding_box(
                row,
                esacci_lakes_static_lake_mask_ds
            )
            esacci_lakes_static_lake_mask_ds_window = sel(
                esacci_lakes_static_lake_mask_ds,
                geo_bounding_box
            )

            esacci_lakes_static_lake_mask = esacci_lakes_static_lake_mask_ds_window["CCI_lakeid"] == row.Index
            assert isinstance(esacci_lakes_static_lake_mask, xr.DataArray)

            with conn.cursor() as cur:
                query = psycopg.sql.SQL("""
                    INSERT INTO esacci_lakes
                    (
                        id,
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
                        geom
                    ) VALUES
                    (
                        %(id)s,
                        %(short_name)s,
                        %(name)s,
                        %(country)s,
                        %(max_distance_to_land)s,
                        %(lat_min_box)s,
                        %(lat_max_box)s,
                        %(lon_min_box)s,
                        %(lon_max_box)s,
                        %(lat_centre)s,
                        %(lon_centre)s,
                        %(lwl_data)s,
                        %(lwe_data)s,
                        %(lswt_data)s,
                        %(lic_data)s,
                        %(lwlr_data)s,
                        %(type)s,
                        ST_GEOMFROMWKB(%(geom)s, 4326)
                    )
                    """
                )

                cur.execute(
                    query,
                    params={
                        "id":                   row.Index,
                        "short_name":           row.short_name,
                        "name":                 row.name,
                        "country":              row.country,
                        "max_distance_to_land": row.max_distance_to_land,
                        "lat_min_box":          row.lat_min_box,
                        "lat_max_box":          row.lat_max_box,
                        "lon_min_box":          row.lon_min_box,
                        "lon_max_box":          row.lon_max_box,
                        "lat_centre":           row.lat_centre,
                        "lon_centre":           row.lon_centre,
                        "lwl_data":             row.lwl_data,
                        "lwe_data":             row.lwe_data,
                        "lswt_data":            row.lswt_data,
                        "lic_data":             row.lic_data,
                        "lwlr_data":            row.lwlr_data,
                        "type":                 row.type,
                        "geom":                 psycopg.Binary(to_wkb(esacci_lakes_static_lake_mask))
                    }
                )

    return RETURN_SUCCESS


# ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
