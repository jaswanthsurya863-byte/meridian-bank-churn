# ============================================================
# Meridian Bank Churn — Step 6: Train ML Model
# ============================================================
# What this script does:
#   1. Loads processed data from DuckDB
#   2. Prepares features for ML
#   3. Trains XGBoost churn prediction model
#   4. Evaluates performance
#   5. Saves model + SHAP explainer for Streamlit app

import duckdb
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, roc_auc_score,
                             confusion_matrix)
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import shap

print("✅ Packages loaded")

# ── 1. Load data from DuckDB ─────────────────────────────────
con = duckdb.connect("meridian.duckdb")
df = con.execute("SELECT * FROM fact_customers").df()
con.close()
print(f"✅ Loaded {len(df):,} rows from DuckDB")

# ── 2. Feature Engineering ───────────────────────────────────
# Select features the model will learn from
feature_cols = [
    'CreditScore', 'Age', 'Tenure', 'Balance',
    'NumOfProducts', 'HasCrCard', 'IsActiveMember',
    'EstimatedSalary', 'geography_key', 'Gender'
]

# Encode Gender (Male=1, Female=0)
df['Gender'] = (df['Gender'] == 'Male').astype(int)

X = df[feature_cols].copy()
y = df['is_churned'].values

print(f"\n📊 Features: {X.shape[1]}")
print(f"📊 Churn rate: {y.mean():.2%}")

# ── 3. Train/Test Split ──────────────────────────────────────
# 80% training, 20% testing — stratify keeps churn rate equal
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n✅ Train: {len(X_train):,} rows | Test: {len(X_test):,} rows")

# ── 4. Train XGBoost Model ───────────────────────────────────
# scale_pos_weight handles class imbalance
# (more non-churners than churners in data)
neg, pos = np.bincount(y_train)
scale = neg / pos

model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    scale_pos_weight=scale,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='auc',
    early_stopping_rounds=20,
    verbosity=0
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)
print("✅ Model trained!")

# ── 5. Evaluate ──────────────────────────────────────────────
y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred = (y_pred_proba >= 0.5).astype(int)

auc = roc_auc_score(y_test, y_pred_proba)
print(f"\n📊 ROC-AUC Score: {auc:.4f}")
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred,
      target_names=['Retained', 'Churned']))

# ── 6. SHAP Explainer ────────────────────────────────────────
print("\n🔍 Computing SHAP values...")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
print("✅ SHAP explainer ready")

# ── 7. Save Everything ───────────────────────────────────────
with open("models/xgb_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/shap_explainer.pkl", "wb") as f:
    pickle.dump(explainer, f)

# Save test predictions for app
X_test_out = X_test.copy()
X_test_out['actual_churn'] = y_test
X_test_out['churn_probability'] = y_pred_proba
X_test_out.to_csv("data/processed/model_predictions.csv", index=False)

print("\n✅ Model saved to models/xgb_model.pkl")
print("✅ Predictions saved to data/processed/model_predictions.csv")
print(f"\n🎯 Final AUC: {auc:.4f} — Model is ready for Streamlit!")
