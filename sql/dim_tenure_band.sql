-- ============================================================
-- Dimension Table: dim_tenure_band
-- ============================================================
-- What this does:
--   Groups customers by how long they've been with the bank
--
-- Tenure = number of years as a customer
--   New      = less than 1 year  (Tenure = 0)
--   Established = 1 to 5 years
--   Loyal    = more than 5 years
-- ============================================================

CREATE OR REPLACE TABLE dim_tenure_band AS
SELECT
    tenure_band,
    sort_order
FROM (
    VALUES
        ('New (< 1 yr)',        1),
        ('Established (1-5 yr)', 2),
        ('Loyal (5+ yr)',       3)
) AS t(tenure_band, sort_order);
