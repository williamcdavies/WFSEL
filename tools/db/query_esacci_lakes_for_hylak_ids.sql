-- query_esacci_lakes_for_hylak_ids.sql

-- Description: Queries HYDROLakes v1.0 polygons against ESA Lakes
--     Climate Change Initiative (Lakes_cci): Lake products, Version 3.0
--     centroid data to match `hylak_id`s to `esacci_lakes_id`s. 

-- Of the 667 lakes in the candidate set, 15 do not have `hylak_id`
-- where a `esacci_lakes_id` is present. The `esacci_lakes_id`s of these
-- 15 are as follows: [141, 143, 149, 211, 293, 317, 363, 420, 451, 473,
-- 507, 512, 581, 2132, 3171]

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
    )

    SELECT
        x2.id AS "esacci_lakes_id",
        x1.id AS "hylak_id"
    FROM x2
    LEFT JOIN x1
        ON ST_COVERS(x1.geom, x2.geom)
    ORDER BY x2.id
) TO STDOUT WITH (FORMAT csv, HEADER);
