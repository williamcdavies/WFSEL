r"""
queries.py

Description:
    Provides definitions for esacci_lakes-utility queries.

Written by William Chuter-Davies
"""

# Related Third-party Imports
from psycopg import sql


# Queries
# ==================================================================================================
DISTINCT_START_DAYS_QUERY = sql.SQL("""
SELECT DISTINCT
    s.start_day AS "day"
FROM {table} AS s
JOIN esacci_lakes AS l
    ON
        ST_INTERSECTS(s.geom, l.geom)
WHERE l.id = %(id)s
    AND s.density > 1
ORDER BY s.start_day
""")


# ==================================================================================================
