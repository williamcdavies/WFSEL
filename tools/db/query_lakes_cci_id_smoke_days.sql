-- query_lakes_cci_id_smoke_days.sql

-- Description: 
--     Queries `spatial.hms_smokes` for the smoke days of a single lake.

-- Parameters
--     lakes_cci_id
--         lakes_cci_id as provided by ESA Lakes Climate Change
--         Initiative (Lakes_cci): Lake products, Version 3.0

--     hms_smokes_table
--         One of ['hms_smokes2005', 
--                 'hms_smokes2006', 
--                 'hms_smokes2007', 
--                 'hms_smokes2008', 
--                 'hms_smokes2009', 
--                 'hms_smokes2010', 
--                 'hms_smokes2011', 
--                 'hms_smokes2012', 
--                 'hms_smokes2013', 
--                 'hms_smokes2014', 
--                 'hms_smokes2015', 
--                 'hms_smokes2016', 
--                 'hms_smokes2017', 
--                 'hms_smokes2018', 
--                 'hms_smokes2019', 
--                 'hms_smokes2020', 
--                 'hms_smokes2021', 
--                 'hms_smokes2022', 
--                 'hms_smokes2023', 
--                 'hms_smokes2023', 
--                 'hms_smokes2025']

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