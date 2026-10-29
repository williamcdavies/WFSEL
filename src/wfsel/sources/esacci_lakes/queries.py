"""
Filename:   wfsel.sources.esacci_lakes.queries.py
Author:     William Chuter-Davies
Modified:   27/10/26
"""

# Related Third-party Imports
import pandas as pd
import psycopg

from psycopg import sql

DISTINCT_START_DAYS_QUERY = sql.SQL("""
SELECT DISTINCT
    s.start_day AS "day"
FROM {table} AS s
JOIN esacci_lakes AS l
    ON
        ST_INTERSECTS(
            s.geom,
            l.geom
        )
WHERE l.id = %(id)s
    AND s.density > 1
ORDER BY s.start_day
""")


def query_distinct_start_days(
    esacci_lakes_id:    int,
    year:               int,
    connection:         psycopg.Connection,
) -> pd.Series[int]:
    """
    Query the distinct start days of a lake by its id and a year.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    year : int
        The year
    connection : psycopg.Connection
        The connection

    Returns
    -------
    pd.Series[int]
        A distinct labels series
    """
    query = DISTINCT_START_DAYS_QUERY.format(table = sql.Identifier(f"hms_smokes{year}"))

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            {
                "id": esacci_lakes_id,
            },
        )

        distinct_start_days_ser = pd.Series(
                                    [
                                        record[0]
                                        for record
                                        in cursor.fetchall()
                                    ],
                                )

    return distinct_start_days_ser
