# Meridian Bank — Customer Churn Diagnostic Analysis

## Business Context
Meridian Bank's churn rate jumped from a 16% baseline to **20.4%** over recent quarters.
This project is a diagnostic analytics case study to answer four questions for the CRO:
- **Where** is churn concentrated?
- **What** is driving it?
- **Which** customers to prioritise for retention?
- **What** early indicators to monitor?

## Live Dashboard
👉 [View on Tableau Public](https://public.tableau.com/app/profile/jaswanth.surya.theja.jeldi/viz/MeridianBankCustomerChurnAnalysis/Dashboard1)

## Key Findings
| Finding | Insight |
|---|---|
| 🇩🇪 Germany churn rate | **32.4%** — 2x higher than France & Spain |
| 📦 3+ Product customers | **85.9%** churn rate — most alarming segment |
| 😴 Inactive members | **26.8%** churn vs 14.3% for active members |
| 🎯 Highest risk cohort | Age 45-60, any tenure band |

## Tech Stack
| Layer | Tool |
|---|---|
| Database | DuckDB |
| Data Processing | Python, Pandas |
| SQL Modeling | Star Schema (fact + 4 dims) |
| Visualisation | Tableau Public |
| ML Layer (Weekend 2) | Scikit-learn, SHAP, Streamlit |

## Project Structure
```
meridian-bank-churn/
├── data/
│   ├── raw/                        # Original Kaggle dataset
│   └── processed/                  # Tableau-ready export
├── sql/
│   ├── dim_geography.sql
│   ├── dim_age_band.sql
│   ├── dim_tenure_band.sql
│   ├── dim_product_segment.sql
│   ├── fact_customers.sql
│   ├── query_01_overall_churn.sql
│   ├── query_02_churn_by_geography.sql
│   ├── query_03_churn_by_products.sql
│   ├── query_04_active_vs_inactive.sql
│   ├── query_05_cohort_matrix.sql
│   └── export_powerbi_wide.sql
├── notebooks/
│   ├── 01_sanity_check.py
│   ├── 02_build_star_schema.py
│   ├── 03_run_diagnostics.py
│   └── 04_export_tableau.py
└── docs/
    └── Meridian Bank Case Brief.docx
```

## Dataset
[Kaggle — Bank Customer Churn Prediction](https://www.kaggle.com/datasets/shubhammeshram579/bank-customer-churn-prediction)
- 10,000 rows, 14 columns
- Overall churn rate: 20.37%
