-- query_esacci_lakes_average_depths.sql

-- Description: Queries average depth for all lakes in
--     spatial.esacci_lakes (Same lakes as provided by as provided by
--     ESA Lakes Climate Change Initiative (esacci_lakes): Lake
--     products, Version 3.0)

-- Written by William Chuter-Davies

COPY (
    WITH x1 AS (
        SELECT
            lp.id AS "id",
            lp.geom_4326 AS "geom"
        FROM lakes AS l
        JOIN lakes_polys AS lp
            ON lp.id = l.id
    ),

    x2 AS (
        SELECT
            l.id AS "id",
            ST_SETSRID(
                ST_MAKEPOINT(
                    l.lon_centre,
                    l.lat_centre
                ),
                4326
            ) AS "geom"
        FROM esacci_lakes AS l
    ),

    x3 AS (
        SELECT
            x2.id AS "esacci_lakes_id",
            x1.id AS "hylak_id"
        FROM x2
        LEFT JOIN x1
            ON ST_COVERS(x1.geom, x2.geom)
    )

    SELECT
        x3.esacci_lakes_id AS "esacci_lakes_id",
        h.depth_avg AS "depth_avg"
    FROM x3
    LEFT JOIN hylak_points AS h
        ON h.hylak_id = x3.hylak_id
    ORDER BY x3.esacci_lakes_id ASC
) TO STDOUT WITH (FORMAT csv, HEADER);
