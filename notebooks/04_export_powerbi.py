# ============================================================
# Meridian Bank Churn — Step 5: Export for Power BI
# ============================================================

import duckdb

con = duckdb.connect("meridian.duckdb")
print("✅ Connected to meridian.duckdb")

# Read and run the export SQL
with open("sql/export_powerbi_wide.sql", "r") as f:
    sql = f.read()

df = con.execute(sql).df()

# ── Quick check before saving ────────────────────────────────
print(f"\n📊 Export shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"\n📋 Columns in export:")
for col in df.columns:
    print(f"   • {col}")

print(f"\n👀 First 3 rows preview:")
print(df.head(3).to_string(index=False))

# ── Confirm churn rate is preserved ─────────────────────────
churn_rate = df['is_churned'].mean() * 100
print(f"\n💡 Churn rate in export: {churn_rate:.2f}% (should be 20.37%)")

# ── Save to CSV ──────────────────────────────────────────────
output_path = "data/processed/meridian_powerbi_ready.csv"
df.to_csv(output_path, index=False)
print(f"\n✅ Saved to: {output_path}")
print(f"   File size: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

con.close()
print("\n🎉 Power BI export complete — ready to import!")
