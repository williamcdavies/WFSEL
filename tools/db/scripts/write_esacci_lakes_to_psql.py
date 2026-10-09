r"""
write_esacci_lakes_to_psql.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

# Related Third-party Imports
import pandas as pd
import psycopg
import xarray as xr

from psycopg import sql

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.geo  import (
    get_esacci_lakes_id_mask,
    get_geo_bounding_box_from_esacci_lakes_static_lake_mask
)
from lib.esacci_lakes.utils.proc import (
    add_argument_esacci_lakes_metadata_csv_path,
    add_argument_esacci_lakes_static_lake_mask_nc_path,
    argument_esacci_lakes_metadata_csv_path_exists,
    argument_esacci_lakes_static_lake_mask_nc_path_exists,
    read_esacci_lakes_metadata_csv
)
from lib.geo.utils               import (
    get_da_geometry_as_wkb,
    select_ds_by_geo_bounding_box
)
from lib.proc.utils              import (
    arguments_are_valid as _arguments_are_valid,
    build_parser        as _build_parser
)
from lib.proc.vars               import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)


# Constants
# ==================================================================================================
PROG  = "write_esacci_lakes_to_psql.py"
QUERY = sql.SQL("""
INSERT INTO esacci_lakes_test
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
""")


# ==================================================================================================


# Parser functions
# ==================================================================================================
def build_parser(
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    return _build_parser(
        PROG,
        "Writes ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0 metadata and geometries to psql for use with PostGIS.",
        positional_arguments = [
            add_argument_esacci_lakes_metadata_csv_path,
            add_argument_esacci_lakes_static_lake_mask_nc_path
        ]
    )


# ==================================================================================================


# Validator functions
# ==================================================================================================
def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Parameters
    ----------
    args : :class:`argparse.Namespace`
        The arguments

    Returns
    -------
    `True` if all arguments are successfully validated. `False` otherwise.
    """
    return _arguments_are_valid(
        args,
        [
            (
                argument_esacci_lakes_metadata_csv_path_exists,
                "esacci_lakes_metadata_csv_path"
            ),
            (
                argument_esacci_lakes_static_lake_mask_nc_path_exists,
                "esacci_lakes_static_lake_mask_nc_path"
            )
        ]
    )


# ==================================================================================================


# Write functions
# ==================================================================================================
def write_esacci_lake_to_psql(
    esacci_lakes_id:                  int,
    esacci_lakes_metadata_df:         pd.DataFrame,
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
    conn:                             psycopg.Connection
) -> None:
    """
    Writes `esacci_lakes_id`'s metadata and geometry to the "esacci_lakes"
    table.

    Parameters
    ----------
    esacci_lakes_id : :class:`int`
        The ESA CCI Lakes id

    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    conn : :class:`psycopg.Connection`
        The connection

    Returns
    -------
    None.
    """
    (
        lat_max_box,
        lat_min_box,
        lon_max_box,
        lon_min_box
    ) = esacci_lakes_metadata_df.loc[
        esacci_lakes_id,
        [
            "lat_max_box",
            "lat_min_box",
            "lon_max_box",
            "lon_min_box"
        ]
    ]

    geo_bounding_box = get_geo_bounding_box_from_esacci_lakes_static_lake_mask(
        esacci_lakes_static_lake_mask_ds,
        lat_max_box = lat_max_box,
        lat_min_box = lat_min_box,
        lon_max_box = lon_max_box,
        lon_min_box = lon_min_box
    )

    static_lake_mask_ds_window = select_ds_by_geo_bounding_box(
        esacci_lakes_static_lake_mask_ds,
        geo_bounding_box
    )

    id_mask = get_esacci_lakes_id_mask(
        esacci_lakes_id,
        static_lake_mask_ds_window
    )

    row = esacci_lakes_metadata_df.loc[esacci_lakes_id]

    with conn.cursor() as cur:
        cur.execute(
            QUERY,
            params = {
                "id":                   esacci_lakes_id,
                "short_name":           row["short_name"],
                "name":                 row["name"],
                "country":              row["country"],
                "max_distance_to_land": row["max_distance_to_land"],
                "lat_min_box":          row["lat_min_box"],
                "lat_max_box":          row["lat_max_box"],
                "lon_min_box":          row["lon_min_box"],
                "lon_max_box":          row["lon_max_box"],
                "lat_centre":           row["lat_centre"],
                "lon_centre":           row["lon_centre"],
                "lwl_data":             row["lwl_data"],
                "lwe_data":             row["lwe_data"],
                "lswt_data":            row["lswt_data"],
                "lic_data":             row["lic_data"],
                "lwlr_data":            row["lwlr_data"],
                "type":                 row["type"],
                "geom":                 psycopg.Binary(get_da_geometry_as_wkb(id_mask))
            }
        )


def write_esacci_lakes_to_psql(
    esacci_lakes_metadata_df:         pd.DataFrame,
    esacci_lakes_static_lake_mask_ds: xr.Dataset,
    conn:                             psycopg.Connection
) -> None:
    """
    Writes each of `esacci_lakes_metadata_df`'s lakes to the "esacci_lakes"
    table.

    Parameters
    ----------
    esacci_lakes_metadata_df : :class:`pandas.DataFrame`
        The ESA CCI Lakes metadata

    esacci_lakes_static_lake_mask_ds : :class:`xarray.Dataset`
        The ESA CCI Lakes static lake mask

    conn : :class:`psycopg.Connection`
        The connection

    Returns
    -------
    None.
    """
    for esacci_lakes_id in esacci_lakes_metadata_df.index:
        write_esacci_lake_to_psql(
            esacci_lakes_id,
            esacci_lakes_metadata_df,
            esacci_lakes_static_lake_mask_ds,
            conn
        )


# ==================================================================================================


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    esacci_lakes_metadata_df = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)

    with (
        xr.open_dataset(args.esacci_lakes_static_lake_mask_nc_path) as esacci_lakes_static_lake_mask_ds,
        psycopg.connect("dbname=spatial")                           as conn
    ):
        write_esacci_lakes_to_psql(
            esacci_lakes_metadata_df,
            esacci_lakes_static_lake_mask_ds,
            conn
        )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
