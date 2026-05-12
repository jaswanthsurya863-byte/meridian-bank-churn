-- ============================================================
-- Dimension Table: dim_age_band
-- ============================================================
-- What this does:
--   Groups customers into age buckets for Power BI slicers
--
-- CASE WHEN = SQL's version of if/else
--   "IF age < 30 THEN label it 'Under 30'"
--   "IF age between 30-45 THEN label it '30-45'"
--   etc.
--
-- sort_order = controls how Power BI sorts the bands
--   (so it shows Under 30, 30-45, 45-60, 60+ in order)
-- ============================================================

CREATE OR REPLACE TABLE dim_age_band AS
SELECT
    age_band,
    sort_order
FROM (
    VALUES
        ('Under 30', 1),
        ('30-45',    2),
        ('45-60',    3),
        ('60+',      4)
) AS t(age_band, sort_order);
