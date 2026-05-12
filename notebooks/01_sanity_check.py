# ============================================================
# Meridian Bank Churn — Step 2: Load & Sanity Check
# ============================================================
# What this script does:
#   1. Connects to DuckDB (creates a local database file)
#   2. Loads our CSV into DuckDB as a table
#   3. Runs sanity checks — row count, columns, nulls
#   4. Confirms overall churn rate

import duckdb  # our analytical database
import pandas as pd  # for displaying results nicely

# ── 1. Connect to DuckDB ────────────────────────────────────
# This creates a file called meridian.duckdb in your project
# Think of it like an Excel file but for a database
con = duckdb.connect("meridian.duckdb")
print("✅ Connected to DuckDB")

# ── 2. Load the CSV into DuckDB ─────────────────────────────
# CREATE OR REPLACE TABLE = "make a new table, overwrite if exists"
# AS SELECT * FROM = "fill it with everything from this file"
con.execute("""
    CREATE OR REPLACE TABLE raw_customers AS
    SELECT * FROM read_csv_auto('data/raw/churn_raw.csv')
""")
print("✅ CSV loaded into table: raw_customers")

# ── 3. Row Count Check ──────────────────────────────────────
# Should be exactly 10,000
row_count = con.execute("SELECT COUNT(*) FROM raw_customers").fetchone()[0]
print(f"\n📊 Row count: {row_count:,}")
if row_count == 10000:
    print("   ✅ Perfect — exactly 10,000 rows")
else:
    print("   ⚠️  Unexpected row count — check your CSV")

# ── 4. Column Names & Types ─────────────────────────────────
# DESCRIBE = show me all column names and their data types
print("\n📋 Column types:")
col_info = con.execute("DESCRIBE raw_customers").df()
print(col_info[['column_name', 'column_type']].to_string(index=False))

# ── 5. First 5 Rows ─────────────────────────────────────────
# Just to visually confirm the data looks right
print("\n👀 First 5 rows:")
preview = con.execute("SELECT * FROM raw_customers LIMIT 5").df()
print(preview.to_string(index=False))

# ── 6. Null Check ───────────────────────────────────────────
# We want to know if any column has missing values
# If nulls = 0 across all columns, our data is clean
print("\n🔍 Null check (should all be 0):")
cols = con.execute("DESCRIBE raw_customers").df()['column_name'].tolist()

null_query = ", ".join([f"SUM(CASE WHEN \"{c}\" IS NULL THEN 1 ELSE 0 END) AS \"{c}\"" for c in cols])
nulls = con.execute(f"SELECT {null_query} FROM raw_customers").df()
print(nulls.T.rename(columns={0: 'null_count'}))

# ── 7. Churn Rate ───────────────────────────────────────────
# AVG(Exited) works because Exited is 0 or 1
# Average of 0s and 1s = percentage of 1s = churn rate
churn = con.execute("""
    SELECT
        COUNT(*)                          AS total_customers,
        SUM(Exited)                       AS churned,
        ROUND(AVG(Exited) * 100, 2)       AS churn_rate_pct
    FROM raw_customers
""").df()

print("\n💡 Overall Churn Rate:")
print(churn.to_string(index=False))

con.close()
print("\n✅ Sanity check complete — ready for Step 3!")
