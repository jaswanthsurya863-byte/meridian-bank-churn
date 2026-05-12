-- ============================================================
-- Fact Table: fact_customers
-- ============================================================
-- This is the centre of the star schema.
-- One row per customer. Connects to all 4 dimension tables.
--
-- Key concepts used here:
--
-- LEFT JOIN = "keep all rows from the left table, and bring
--   in matching data from the right table"
--   We use this to attach geography_key from dim_geography
--
-- CASE WHEN = if/else logic to assign age bands and tenure bands
--
-- The fact table stores:
--   - The customer's key metrics (balance, score, etc.)
--   - Foreign keys linking to each dimension table
--   - The target: Exited (1 = churned, 0 = stayed)
-- ============================================================

CREATE OR REPLACE TABLE fact_customers AS
SELECT
    -- Customer identifiers
    rc.CustomerId,

    -- Foreign key to dim_geography
    dg.geography_key,

    -- Age band label (CASE WHEN = if/else)
    CASE
        WHEN rc.Age < 30            THEN 'Under 30'
        WHEN rc.Age BETWEEN 30 AND 45 THEN '30-45'
        WHEN rc.Age BETWEEN 46 AND 60 THEN '45-60'
        ELSE                             '60+'
    END AS age_band,

    -- Tenure band label
    CASE
        WHEN rc.Tenure = 0          THEN 'New (< 1 yr)'
        WHEN rc.Tenure BETWEEN 1 AND 5 THEN 'Established (1-5 yr)'
        ELSE                            'Loyal (5+ yr)'
    END AS tenure_band,

    -- Product segment label
    CASE
        WHEN rc.NumOfProducts = 1   THEN '1 Product'
        WHEN rc.NumOfProducts = 2   THEN '2 Products'
        ELSE                             '3+ Products'
    END AS product_segment,

    -- Customer metrics (the measurable facts)
    rc.CreditScore,
    rc.Age,
    rc.Tenure,
    rc.Balance,
    rc.NumOfProducts,
    rc.HasCrCard,
    rc.IsActiveMember,
    rc.EstimatedSalary,
    rc.Gender,

    -- The target variable: 1 = churned, 0 = stayed
    rc.Exited                       AS is_churned

FROM raw_customers rc

-- LEFT JOIN brings in geography_key from dim_geography
-- ON = the matching condition between the two tables
LEFT JOIN dim_geography dg
    ON rc.Geography = dg.country;
