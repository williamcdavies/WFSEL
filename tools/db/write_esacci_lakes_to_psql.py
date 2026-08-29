r"""
write_esacci_lakes_to_psql.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import ArgumentParser

# Related Third-party Imports
import psycopg
import xarray as xr

from tqdm import tqdm

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils import (
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists,
    bounding_box,
    wkb,
    read_esacci_lakes_metadata_csv,
)
from lib.io.vars import RETURN_FAILURE, RETURN_SUCCESS

PROG = "write_esacci_lakes_to_psql.py"


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog=f"{PROG}.py",
        usage="%(prog)s [options]",
        description="""Writes ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0 metadata and geometries to psql for use with PostGIS.""",
    )

    # Positional arguments
    add_argument_esacci_lakes_static_lake_mask_nc_path(parser)
    add_argument_esacci_lakes_metadata_csv_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not argument_esacci_lakes_metadata_csv_path_exists(
        args.esacci_lakes_metadata_csv_path, loud=True
    ):
        return RETURN_FAILURE

    if not argument_esacci_lakes_static_lake_mask_nc_path_exists(
        args.esacci_lakes_static_lake_mask_nc_path, loud=True
    ):
        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    esacci_lakes_metadata_df = read_esacci_lakes_metadata_csv(
        args.esacci_lakes_metadata_csv_path
    )

    with (
        xr.open_dataset(
            args.esacci_lakes_static_lake_mask_nc_path
        ) as esacci_lakes_static_lake_mask_ds,
        psycopg.connect("dbname=spatial") as conn,
    ):
        for row in tqdm(
            esacci_lakes_metadata_df.itertuples(), total=len(esacci_lakes_metadata_df)
        ):
            lat_max_box, lat_min_box, lon_max_box, lon_min_box = bounding_box(
                row, esacci_lakes_static_lake_mask_ds
            )

            esacci_lakes_static_lake_mask = (
                esacci_lakes_static_lake_mask_ds["CCI_lakeid"].sel(
                    lat=slice(lat_min_box, lat_max_box),
                    lon=slice(lon_min_box, lon_max_box),
                )
                == row.Index
            )
            assert isinstance(esacci_lakes_static_lake_mask, xr.DataArray)

            with conn.cursor() as cur:
                cur.execute(
                    """
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
                        %s, 
                        ST_GEOMFROMWKB(%s, 4326)
                    )""",
                    (
                        row.Index,
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
                        psycopg.Binary(wkb(esacci_lakes_static_lake_mask)),
                    ),
                )

    return RETURN_SUCCESS


# ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
