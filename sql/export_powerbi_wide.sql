-- ============================================================
-- Export: Power BI Wide Table
-- ============================================================
-- Business purpose:
--   Power BI imports one clean flat file — no SQL joins needed
--   This query combines fact_customers + all dimension labels
--   into a single wide table ready for drag-and-drop visuals
--
-- New concept:
--   CTE (Common Table Expression) = a named temporary query
--   Written as: WITH name AS (SELECT ...)
--   Think of it like giving a subquery a nickname so you can
--   refer to it later — keeps long queries readable
--
-- We use a CTE here to calculate the churn label cleanly
--   before the final SELECT
-- ============================================================

-- CTE: enrich the fact table with all labels in one place
WITH enriched AS (
    SELECT
        -- Customer ID
        fc.CustomerId,

        -- Geography (from dim_geography)
        dg.country                          AS geography,

        -- Age info
        fc.Age,
        fc.age_band,
        dab.sort_order                      AS age_band_sort,

        -- Tenure info
        fc.Tenure,
        fc.tenure_band,
        dtb.sort_order                      AS tenure_band_sort,

        -- Product info
        fc.NumOfProducts,
        fc.product_segment,
        dps.sort_order                      AS product_segment_sort,

        -- Financial metrics
        fc.CreditScore,
        fc.Balance,
        fc.EstimatedSalary,

        -- Membership info
        fc.Gender,
        fc.HasCrCard,
        fc.IsActiveMember,

        -- Activity label (readable)
        CASE
            WHEN fc.IsActiveMember = 1 THEN 'Active'
            ELSE 'Inactive'
        END                                 AS member_status,

        -- Credit card label (readable)
        CASE
            WHEN fc.HasCrCard = 1 THEN 'Has Credit Card'
            ELSE 'No Credit Card'
        END                                 AS credit_card_status,

        -- The target variable
        fc.is_churned,

        -- Churn label (readable) — for Power BI slicers
        CASE
            WHEN fc.is_churned = 1 THEN 'Churned'
            ELSE 'Retained'
        END                                 AS churn_label

    FROM fact_customers fc

    -- Join all 4 dimension tables
    JOIN dim_geography       dg  ON fc.geography_key   = dg.geography_key
    JOIN dim_age_band        dab ON fc.age_band         = dab.age_band
    JOIN dim_tenure_band     dtb ON fc.tenure_band      = dtb.tenure_band
    JOIN dim_product_segment dps ON fc.product_segment  = dps.product_segment
)

-- Final SELECT from the CTE — this is what gets exported
SELECT * FROM enriched
ORDER BY CustomerId;
