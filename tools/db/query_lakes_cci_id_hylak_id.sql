-- query_lakes_cci_id_hylak_id.sql

-- Description: 
--     Queries HYDROLakes v1.0 polygons against ESA Lakes
--     Climate Change Initiative (Lakes_cci): Lake products, Version 3.0
--     centroid data to match `hylak_id`s to `lakes_cci_id`s. 

-- Of the 667 lakes in the candidate set, 15 do not have `hylak_id`
-- where a `lakes_cci_id` is present. The `lake_cci_id`s of these 15 are
-- as follows: [141, 143, 149, 211, 293, 317, 363, 420, 451, 473, 507,
-- 512, 581, 2132, 3171]

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
    )
    SELECT
        x2.gid AS "lakes_cci_id",
        x1.gid AS "hylak_id"
    FROM x2
    LEFT JOIN x1
        ON ST_Covers(x1.geom, x2.geom)
    ORDER BY x2.gid
) TO STDOUT WITH (FORMAT CSV, HEADER);