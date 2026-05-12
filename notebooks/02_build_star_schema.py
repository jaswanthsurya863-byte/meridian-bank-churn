# ============================================================
# Meridian Bank Churn — Step 3: Build Star Schema
# ============================================================
# Reads each .sql file and runs it against our DuckDB database

import duckdb

# Connect to the SAME database file we created in Step 2
con = duckdb.connect("meridian.duckdb")
print("✅ Connected to meridian.duckdb")

# List of SQL files to run in order
# (dim tables must be built before fact table)
sql_files = [
    "sql/dim_geography.sql",
    "sql/dim_age_band.sql",
    "sql/dim_tenure_band.sql",
    "sql/dim_product_segment.sql",
    "sql/fact_customers.sql",
]

# Loop through each file, read it, and execute it
for filepath in sql_files:
    with open(filepath, "r") as f:
        sql = f.read()          # read the SQL text
    con.execute(sql)            # run it in DuckDB
    table_name = filepath.split("/")[-1].replace(".sql", "")
    print(f"✅ Built: {table_name}")

# ── Verify all tables exist ──────────────────────────────────
print("\n📋 Tables now in meridian.duckdb:")
tables = con.execute("SHOW TABLES").df()
print(tables.to_string(index=False))

# ── Quick row count check ────────────────────────────────────
print("\n📊 Row counts:")
for table in tables['name']:
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"   {table}: {count:,} rows")

# ── Preview fact table ───────────────────────────────────────
print("\n👀 Fact table preview (first 3 rows):")
preview = con.execute("""
    SELECT CustomerId, geography_key, age_band,
           tenure_band, product_segment, Balance,
           is_churned
    FROM fact_customers
    LIMIT 3
""").df()
print(preview.to_string(index=False))

con.close()
print("\n✅ Star schema built successfully!")
