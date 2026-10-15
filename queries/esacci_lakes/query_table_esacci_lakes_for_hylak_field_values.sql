-- query_table_esacci_lakes_for_hylak_field_values.sql

-- Description: Queries spatial.esacci_lakes and spatial.hylak_polys for
--      HydroLAKES field values for all lakes in the candidate set (as
--      provided by ESA Lakes Climate Change Initiative (Lakes_cci):
--      Lake products, Version 3.0). Metric fields are scaled to base SI
--      units. Fields are suffixed with their unit for clarity.

-- Of the 667 lakes in the candidate set, 15 do not have `hylak_id`
-- where a `esacci_lakes_id` is present. The `esacci_lakes_id`s of these
-- 15 are as follows: [141, 143, 149, 211, 293, 317, 363, 420, 451, 473,
-- 507, 512, 581, 2132, 3171]

-- Written by William Chuter-Davies

COPY (
    WITH x1 AS (
        SELECT
            hp.hylak_id        AS "hylak_id",
            hp.lake_name       AS "lake_name",
            hp.country         AS "country",
            hp.continent       AS "continent",
            hp.poly_src        AS "poly_src",
            hp.lake_type       AS "lake_type",
            hp.grand_id        AS "grand_id",
            hp.lake_area * 1e6 AS "lake_area_m2",     -- convert km2 to m2
            hp.shore_len * 1e3 AS "shore_len_m",      -- convert km  to m
            hp.shore_dev       AS "shore_dev",
            hp.vol_total * 1e6 AS "vol_total_m3",     -- convert mcm to m3
            hp.vol_res   * 1e6 AS "vol_res_m3",       -- convert mcm to m3
            hp.vol_src         AS "vol_src",
            hp.depth_avg       AS "depth_avg_m",
            hp.dis_avg         AS "dis_avg_m3_per_s",
            hp.res_time        AS "res_time_days",
            hp.elevation       AS "elevation_m",
            hp.slope_100       AS "slope_deg",
            hp.wshd_area * 1e6 AS "wshd_area_m2",     -- convert km2 to m2
            hp.pour_long       AS "pour_long_deg",
            hp.pour_lat        AS "pour_lat_deg",
            hp.geom            AS "geom"
        FROM hylak_polys AS hp
    ),

    x2 AS (
        SELECT
            l.id AS "esacci_lakes_id",
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
        x2.esacci_lakes_id  AS "esacci_lakes_id",
        x1.hylak_id         AS "hylak_id",
        x1.lake_name        AS "lake_name",
        x1.country          AS "country",
        x1.continent        AS "continent",
        x1.poly_src         AS "poly_src",
        x1.lake_type        AS "lake_type",
        x1.grand_id         AS "grand_id",
        x1.lake_area_m2     AS "lake_area_m2",
        x1.shore_len_m      AS "shore_len_m",
        x1.shore_dev        AS "shore_dev",
        x1.vol_total_m3     AS "vol_total_m3",
        x1.vol_res_m3       AS "vol_res_m3",
        x1.vol_src          AS "vol_src",
        x1.depth_avg_m      AS "depth_avg_m",
        x1.dis_avg_m3_per_s AS "dis_avg_m3_per_s",
        x1.res_time_days    AS "res_time_days",
        x1.elevation_m      AS "elevation_m",
        x1.slope_deg        AS "slope_deg",
        x1.wshd_area_m2     AS "wshd_area_m2",
        x1.pour_long_deg    AS "pour_long_deg",
        x1.pour_lat_deg     AS "pour_lat_deg"
    FROM x2
    LEFT JOIN x1
        ON
            ST_COVERS(x1.geom, x2.geom)
    ORDER BY x2.esacci_lakes_id
) TO STDOUT WITH (FORMAT csv, HEADER);
