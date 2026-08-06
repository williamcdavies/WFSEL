-- query_lakes_cci_id_smoke_days.sql

-- Description: 
--    Queries `spatial.hms_smokes` for the smoke days of a single lake.

-- Written by William Chuter-Davies


COPY (
    WITH x AS (
        SELECT
            l.gid,
            l.short_name,
            l.name,
            l.geom
        FROM lakes_cci_lakes AS l
        WHERE l.gid = :lakes_cci_id
    )
    SELECT DISTINCT ON (s.start_day)
        x.gid,
        x.short_name,
        x.name,
        s.start_day AS "day"
    FROM :hms_smokes_table AS s
    JOIN x                 AS x
        ON ST_INTERSECTS(s.geom, x.geom)
    WHERE s.density > 1
    ORDER BY s.start_day
)
TO STDOUT WITH (FORMAT CSV, HEADER);