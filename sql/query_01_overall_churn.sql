-- ============================================================
-- Diagnostic Query 1: Overall Churn Rate
-- ============================================================
-- Business question: What is Meridian Bank's current churn rate?
--
-- New concepts:
--   COUNT(*) = count every row
--   SUM(is_churned) = add up all the 1s (churned customers)
--   ROUND(x, 2) = round to 2 decimal places
--   * 100 = convert decimal (0.20) to percentage (20.37)
-- ============================================================

SELECT
    COUNT(*)                            AS total_customers,
    SUM(is_churned)                     AS total_churned,
    COUNT(*) - SUM(is_churned)          AS total_retained,
    ROUND(AVG(is_churned) * 100, 2)     AS churn_rate_pct
FROM fact_customers;
