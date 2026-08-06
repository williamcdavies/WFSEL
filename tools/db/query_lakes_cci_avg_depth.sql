-- query_lakes_cci_avg_depth.sql

-- Description: 

-- Written by William Chuter-Davies

COPY (
    WITH x1 AS (
        SELECT
            lp.gid       AS "gid",
            lp.geom_4326 AS "geom"
        FROM lakes AS l
        JOIN lakes_polys AS lp
            ON lp.gid = l.id
    ),
    x2 AS (
        SELECT
            lakes_cci.gid AS "gid",
            ST_SetSRID(
                ST_MakePoint(lakes_cci.lon_centre, 
                             lakes_cci.lat_centre),
                4326
            )             AS "geom"
        FROM lakes_cci_lakes AS lakes_cci
    ),
    x3 AS (
        SELECT
            x2.gid AS "lakes_cci_id",
            x1.gid AS "hylak_id"
        FROM x2
        LEFT JOIN x1
            ON ST_Covers(x1.geom, x2.geom)
    )
    SELECT
        x3.lakes_cci_id AS "lakes_cci_id",
        h.depth_avg     AS "depth_avg"
    FROM x3
    JOIN hylak AS h
        ON h.hylak_id = x3.hylak_id
    ORDER BY x3.lakes_cci_id ASC
) TO STDOUT WITH (FORMAT CSV, HEADER);