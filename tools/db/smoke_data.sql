WITH x AS (
    SELECT
        lp.geom_4326 AS geom
    FROM lakes       AS l
    JOIN lakes_polys AS lp
    ON l.id = lp.id
    WHERE l.id = 5
)
SELECT
    s.id,
    s.start_year,
    s.start_day,
    s.start_time,
    s.end_year,
    s.end_day,
    s.end_time,
    s.density
FROM hms_smokes2011 AS s
JOIN x              AS x
ON ST_INTERSECTS(s.geom, x.geom)
WHERE s.density > 1
ORDER BY s.start_day;