-- query_counts_of_distinct_start_days_by_year.sql

-- Description: 
--      Queries spatial.umn_lakes and spatial.hms_smokes for counts
--      of distinct start days for all UMN lakes for each year in
--      [2011-2023].

-- Written by William Chuter-Davies

COPY (
    SELECT
        l.unmlknum                                                     AS "umn_lakes_id",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2011) AS "2011",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2012) AS "2012",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2013) AS "2013",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2014) AS "2014",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2015) AS "2015",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2016) AS "2016",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2017) AS "2017",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2018) AS "2018",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2019) AS "2019",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2020) AS "2020",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2021) AS "2021",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2022) AS "2022",
        COUNT(DISTINCT s.start_day) FILTER (WHERE s.start_year = 2023) AS "2023"
    FROM umn_lakes AS l
    LEFT JOIN hms_smokes AS s
        ON
            ST_INTERSECTS(
                s.geom,
                ST_TRANSFORM(l.wkb_geometry, 4326)
            )
            AND s.density > 1
            AND s.start_year BETWEEN 2011 AND 2023
    GROUP BY l.unmlknum
    ORDER BY l.unmlknum
) TO STDOUT WITH (FORMAT csv, HEADER);
