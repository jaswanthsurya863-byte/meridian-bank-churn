-- ============================================================
-- Diagnostic Query 4: Active vs Inactive Member Churn
-- ============================================================
-- Business question: Does being an active member protect
--   against churn?
--
-- New concept:
--   CASE WHEN inside SELECT (not creating a table, just
--   renaming values for readability in the output)
--   IsActiveMember is 0 or 1 — we label it as text
-- ============================================================

SELECT
    CASE
        WHEN IsActiveMember = 1 THEN 'Active'
        ELSE 'Inactive'
    END                                 AS member_status,
    COUNT(*)                            AS total_customers,
    SUM(is_churned)                     AS churned,
    ROUND(AVG(is_churned) * 100, 2)     AS churn_rate_pct
FROM fact_customers

GROUP BY IsActiveMember
ORDER BY IsActiveMember DESC;  -- Active (1) shown first
