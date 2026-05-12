-- ============================================================
-- Diagnostic Query 2: Churn Rate by Geography
-- ============================================================
-- Business question: Which country has the highest churn?
-- Expected finding: Germany ~32%
--
-- New concepts:
--   GROUP BY = split results into groups (one row per country)
--   ORDER BY ... DESC = sort from highest to lowest
--   JOIN = connect fact_customers to dim_geography
--     so we see country names instead of geography_key numbers
-- ============================================================

SELECT
    dg.country,
    COUNT(*)                            AS total_customers,
    SUM(fc.is_churned)                  AS churned,
    ROUND(AVG(fc.is_churned) * 100, 2)  AS churn_rate_pct
FROM fact_customers fc

-- JOIN brings in the country name from dim_geography
JOIN dim_geography dg
    ON fc.geography_key = dg.geography_key

GROUP BY dg.country          -- one row per country
ORDER BY churn_rate_pct DESC; -- highest churn first
