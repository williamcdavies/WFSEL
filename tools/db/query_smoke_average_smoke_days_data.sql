-- query_smoke_days_data.sql

-- Description: 
--    Queries `spatial.lakes`, `spatial.lakes_polys`, and
--    `spatial.hms_smokes` for the average number of smoke days for a
--    given year

-- Notes:
--     id=240 is United States
--     id=61  is Canada

-- Written by William Chuter-Davies


COPY (
    WITH x1 AS (
        SELECT
            l.id
        FROM lakes       AS l
        JOIN lakes_polys AS lp
            ON lp.id = l.id
        WHERE l.country = 240 OR 
              l.country = 61
        ORDER BY ST_AREA(lp.geom_4326) DESC
        LIMIT 1000),
    x2 AS (
        SELECT
            x1.id,
            COUNT(DISTINCT s.start_day) AS "smoke_days"
        FROM x1
        JOIN lakes_polys AS lp
            ON lp.id = x1.id
        LEFT JOIN :hms_smokes_table AS s
            ON ST_INTERSECTS(s.geom, lp.geom_4326)
        GROUP BY x1.id)
    SELECT AVG(x2.smoke_days)
        FROM x2
) TO STDOUT WITH (FORMAT CSV, HEADER)