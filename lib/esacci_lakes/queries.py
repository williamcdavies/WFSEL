r"""
queries.py

Description:
   Provides definitions for esacci_lakes-utility queries.

Written by William Chuter-Davies
"""

# Related Third-party Imports
from psycopg import sql

COUNT_OF_DISTINCT_START_DAYS_QUERY = sql.SQL("""
WITH xref AS (
    SELECT l.geom
    FROM esacci_lakes AS l
    WHERE l.id = %(id)s
)

SELECT DISTINCT ON (s.start_day) s.start_day AS "day"
FROM {table} AS s
JOIN xref AS x
    ON ST_INTERSECTS(s.geom, x.geom)
WHERE s.density > 1
ORDER BY s.start_day
""")
