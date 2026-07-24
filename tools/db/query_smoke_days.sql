-- query_smoke_days.sql

-- Description: 
--    Queries `spatial.hms_smokes` for the smoke days of a single lake.

-- Written by William Chuter-Davies


COPY (
    WITH x AS (
        SELECT
            l.name       AS "name",
            lp.geom_4326 AS "geom"
        FROM lakes       AS l
        JOIN lakes_polys AS lp
        ON l.id = lp.id
        WHERE l.id = :lakes_id
    )
    SELECT
        x.name      AS "name",
        s.start_day AS "day"
    FROM :hms_smokes_table AS s
    JOIN x                 AS x
    ON ST_INTERSECTS(s.geom, x.geom)
    WHERE s.density > 1
    ORDER BY s.start_day
)
TO STDOUT WITH (FORMAT CSV, HEADER);