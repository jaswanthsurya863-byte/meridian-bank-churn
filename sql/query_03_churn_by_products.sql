-- ============================================================
-- Diagnostic Query 3: Churn Rate by Product Count
-- ============================================================
-- Business question: Do customers with more products churn more?
-- Expected finding: 3+ products spikes to ~83% — very alarming!
--
-- New concept:
--   ORDER BY sort_order = uses the sort number from our
--     dimension table to display in logical order
--     (1 Product → 2 Products → 3+ Products)
--     instead of alphabetical order
-- ============================================================

SELECT
    fc.product_segment,
    dps.sort_order,
    COUNT(*)                            AS total_customers,
    SUM(fc.is_churned)                  AS churned,
    ROUND(AVG(fc.is_churned) * 100, 2)  AS churn_rate_pct
FROM fact_customers fc

JOIN dim_product_segment dps
    ON fc.product_segment = dps.product_segment

GROUP BY fc.product_segment, dps.sort_order
ORDER BY dps.sort_order;  -- show in logical order: 1, 2, 3+
