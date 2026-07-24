-- query_smoke_days2.sql

-- Description: 
--    Queries count of smoke days for all lakes in spatial.esa_lakes
--    (Same lakes as provided by as provided by ESA Lakes Climate Change
--    Initiative (Lakes_cci): Lake products, Version 3.0) for each year
--    between 2011--2023 inclusive.

-- | lakes_cci_id | 2011     | $\cdots$ | 2023     |
-- |:------------ |:-------- |:-------- |:-------- |
-- | $i_1$        | $d_{11}$ | $\cdots$ | $d_{1n}$ |
-- | $\vdots$     | $\vdots$ | $\ddots$ | $\vdots$ |
-- | $i_m$        | $d_{m1}$ | $\cdots$ | $d_{mn}$ |

-- Written by William Chuter-Davies

COPY (
    SELECT
        l.id                                                           AS "lakes_cci_id",
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
    FROM esa_lakes AS l
    LEFT JOIN hms_smokes AS s
        ON ST_INTERSECTS(s.geom, l.geom)
        AND s.density    > 1
        AND s.start_year BETWEEN 2011 AND 2023
    GROUP BY l.id
    ORDER BY l.id
) TO STDOUT WITH (FORMAT CSV, HEADER);