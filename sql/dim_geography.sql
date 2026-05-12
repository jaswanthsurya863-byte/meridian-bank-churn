-- ============================================================
-- Dimension Table: dim_geography
-- ============================================================
-- What this does:
--   Pulls every unique country from raw_customers
--   and assigns it a unique ID (geography_key)
--
-- ROW_NUMBER() = assign a sequential number (1, 2, 3...)
-- OVER (ORDER BY Geography) = ordered alphabetically
-- ============================================================

CREATE OR REPLACE TABLE dim_geography AS
SELECT
    ROW_NUMBER() OVER (ORDER BY Geography)  AS geography_key,
    Geography                               AS country
FROM (
    SELECT DISTINCT Geography               -- DISTINCT = no duplicates
    FROM raw_customers
);
