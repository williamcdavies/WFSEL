"""
Filename:   wfsel.sources.noaa_hms.queries.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import geopandas as gpd
import psycopg

from psycopg import sql

HMS_SMOKES_RECORD_EXISTS_QUERY  = sql.SQL("""
SELECT EXISTS (
    SELECT
        1
    FROM hms_smokes AS h
    WHERE h.start_year = %(start_year)s
        AND h.start_day = %(start_day)s
)
""")
HMS_SMOKES_RECORD_DELETE_QUERY  = sql.SQL("""
DELETE FROM hms_smokes
WHERE start_year = %(start_year)s
    AND start_day = %(start_day)s
""")
HMS_SMOKES_RECORD_INSERT_QUERY  = sql.SQL("""
INSERT INTO hms_smokes
    (
        start_year,
        start_day,
        start_time,
        end_year,
        end_day,
        end_time,
        density,
        geom
    )
VALUES
    (
        %(start_year)s,
        %(start_day)s,
        %(start_time)s,
        %(end_year)s,
        %(end_day)s,
        %(end_time)s,
        %(density)s,
        ST_GEOMFROMTEXT(%(geom)s, 4326)
    )
""")


def query_hms_smokes_record_exists(
    start_year: int,
    start_day:  int,
    connection: psycopg.Connection,
) -> bool:
    """
    Query the existence of an hms_smokes record.

    Parameters
    ----------
    start_year : int
        The start year
    start_day : int
        The start day
    connection : psycopg.Connection
        The connection

    Returns
    -------
    bool
        True if the record exists, False otherwise
    """
    with connection.cursor() as cursor:
        cursor.execute(
            HMS_SMOKES_RECORD_EXISTS_QUERY,
            {
                "start_year":   start_year,
                "start_day":    start_day,
            },
        )

        record      = cursor.fetchone()
        (exists,)   = record    # type: ignore[misc]

    return exists


def query_hms_smokes_record_delete(
    start_year: int,
    start_day:  int,
    connection: psycopg.Connection,
) -> None:
    """
    Query the deletion of an hms_smokes record.

    Parameters
    ----------
    start_year : int
        The start year
    start_day : int
        The start day
    connection : psycopg.Connection
        The connection
    """
    with connection.cursor() as cursor:
        cursor.execute(
            HMS_SMOKES_RECORD_DELETE_QUERY,
            {
                "start_year":   start_year,
                "start_day":    start_day,
            },
        )


def query_hms_smokes_record_insert(
    noaa_hms_gdf:   gpd.GeoDataFrame,
    connection:     psycopg.Connection,
) -> None:
    """
    Query the insertion of an hms_smokes record.

    Parameters
    ----------
    noaa_hms_gdf : gpd.GeoDataFrame
        The NOAA HMS geodataframe
    connection : psycopg.Connection
        The connection
    """
    records = [
                {
                    "start_year":   int(row.start_year),    # type: ignore[arg-type]
                    "start_day":    int(row.start_day),     # type: ignore[arg-type]
                    "start_time":   int(row.start_time),    # type: ignore[arg-type]
                    "end_year":     int(row.end_year),      # type: ignore[arg-type]
                    "end_day":      int(row.end_day),       # type: ignore[arg-type]
                    "end_time":     int(row.end_time),      # type: ignore[arg-type]
                    "density":      int(row.density),       # type: ignore[arg-type]
                    "geom":         row.geom.wkt,           # type: ignore[attr-defined]
                }
                for row
                in noaa_hms_gdf.itertuples()
            ]

    with connection.cursor() as cursor:
        cursor.executemany(
            HMS_SMOKES_RECORD_INSERT_QUERY,
            records,
        )
