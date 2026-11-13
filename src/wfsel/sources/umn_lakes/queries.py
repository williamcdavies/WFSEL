"""
Filename:   wfsel.sources.umn_lakes.queries.py
Author:     William Chuter-Davies
"""

# Related Third-party Imports
import pandas as pd
import psycopg

from psycopg import sql

UMN_LAKES_DISTINCT_START_DAYS_QUERY = sql.SQL("""
SELECT DISTINCT
    s.start_day AS "day"
FROM {table} AS s
JOIN public.umn_lakes AS l
    ON
        ST_INTERSECTS(
            s.geom,
            ST_TRANSFORM(
                l.wkb_geometry,
                4326
            )
        )
WHERE l.unmlknum = %(unmlknum)s
    AND s.density > 1
ORDER BY s.start_day
""")


def query_umn_lakes_distinct_start_days(
    umn_lakes_id:   str,
    year:           int,
    connection:     psycopg.Connection,
) -> pd.Series[int]:
    """
    Query the distinct start days of a lake by its id and a year.

    Parameters
    ----------
    umn_lakes_id : str
        The UMN Lakes id
    year : int
        The year
    connection : psycopg.Connection
        The connection

    Returns
    -------
    pd.Series[int]
        A distinct labels series
    """
    query = UMN_LAKES_DISTINCT_START_DAYS_QUERY.format(
        table = sql.Identifier(f"hms_smokes{year}"),
    )

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            {
                "unmlknum": umn_lakes_id,
            },
        )

        records = cursor.fetchall()
        days    = [
                    day
                    for
                    (day,)
                    in records
                ]

        distinct_start_days_ser = pd.Series(days)

    return distinct_start_days_ser
