# ============================================================
# Meridian Bank Churn — Step 4: Run Diagnostic Queries
# ============================================================

import duckdb

con = duckdb.connect("meridian.duckdb")

# Helper: run a .sql file and print results neatly
def run_query(filepath, title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    with open(filepath, "r") as f:
        sql = f.read()
    result = con.execute(sql).df()
    print(result.to_string(index=False))
    return result

run_query("sql/query_01_overall_churn.sql",
          "Q1: Overall Churn Rate")

run_query("sql/query_02_churn_by_geography.sql",
          "Q2: Churn Rate by Geography")

run_query("sql/query_03_churn_by_products.sql",
          "Q3: Churn Rate by Product Count")

run_query("sql/query_04_active_vs_inactive.sql",
          "Q4: Active vs Inactive Member Churn")

run_query("sql/query_05_cohort_matrix.sql",
          "Q5: Cohort Matrix — Age Band x Tenure Band")

con.close()
print("\n✅ All diagnostic queries complete!")
