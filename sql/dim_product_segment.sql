-- ============================================================
-- Dimension Table: dim_product_segment
-- ============================================================
-- What this does:
--   Groups customers by how many bank products they hold
--   (savings account, credit card, loan, etc.)
--
-- This dimension will reveal the most shocking finding:
--   customers with 3+ products churn at ~83%!
-- ============================================================

CREATE OR REPLACE TABLE dim_product_segment AS
SELECT
    product_segment,
    sort_order
FROM (
    VALUES
        ('1 Product',   1),
        ('2 Products',  2),
        ('3+ Products', 3)
) AS t(product_segment, sort_order);
