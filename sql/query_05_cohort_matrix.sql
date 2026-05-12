-- ============================================================
-- Diagnostic Query 5: Cohort Matrix — Age Band × Tenure Band
-- ============================================================
-- Business question: Which combination of age + tenure is
--   the highest churn risk?
--
-- New concept:
--   GROUP BY two columns = creates a grid of combinations
--   This gives us a matrix (like a pivot table in Excel)
--   e.g. "60+ customers who are also New = what % churn?"
--
--   This is the query that finds your most at-risk segment
--   to prioritise for retention campaigns
-- ============================================================

SELECT
    fc.age_band,
    dab.sort_order                      AS age_sort,
    fc.tenure_band,
    dtb.sort_order                      AS tenure_sort,
    COUNT(*)                            AS total_customers,
    SUM(fc.is_churned)                  AS churned,
    ROUND(AVG(fc.is_churned) * 100, 2)  AS churn_rate_pct
FROM fact_customers fc

JOIN dim_age_band dab
    ON fc.age_band = dab.age_band

JOIN dim_tenure_band dtb
    ON fc.tenure_band = dtb.tenure_band

GROUP BY
    fc.age_band, dab.sort_order,
    fc.tenure_band, dtb.sort_order

ORDER BY
    dab.sort_order,    -- age bands in order
    dtb.sort_order;    -- tenure bands in order within each age
