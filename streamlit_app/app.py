# ============================================================
# Meridian Bank — Customer Churn Prediction App
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Meridian Bank Churn Analytics",
    page_icon="🏦",
    layout="wide"
)

# ── Load Model ───────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("models/xgb_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/shap_explainer.pkl", "rb") as f:
        explainer = pickle.load(f)
    return model, explainer

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/model_predictions.csv")

model, explainer = load_model()
df = load_data()

# ── Sidebar Navigation ───────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/bank.png", width=60)
st.sidebar.title("Meridian Bank")
st.sidebar.markdown("**Churn Analytics Platform**")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "📊 Executive Dashboard",
    "🔮 Predict Customer Churn",
    "💰 Business Impact Simulator"
])

# ============================================================
# PAGE 1 — Executive Dashboard
# ============================================================
if page == "📊 Executive Dashboard":

    st.title("🏦 Meridian Bank — Churn Diagnostic Dashboard")
    st.markdown("*Churn jumped from 16% baseline to 20.4% — here's where and why*")
    st.markdown("---")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", "10,000")
    col2.metric("Churn Rate", "20.37%", "+4.37% vs baseline", delta_color="inverse")
    col3.metric("Customers at Risk", "2,037", "Need retention action", delta_color="inverse")
    col4.metric("Model AUC", "0.8632", "Strong predictive power")

    st.markdown("---")

    # Charts row
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Churn Rate by Geography")
        geo_data = pd.DataFrame({
            "Country": ["Germany", "Spain", "France"],
            "Churn Rate": [32.44, 16.67, 16.15]
        })
        fig = px.bar(geo_data, x="Country", y="Churn Rate",
                     color="Churn Rate",
                     color_continuous_scale="Reds",
                     title="Germany churns at 2x the rate of France & Spain")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Churn Rate by Product Count")
        prod_data = pd.DataFrame({
            "Segment": ["1 Product", "2 Products", "3+ Products"],
            "Churn Rate": [27.71, 7.58, 85.89]
        })
        fig2 = px.bar(prod_data, x="Segment", y="Churn Rate",
                      color="Churn Rate",
                      color_continuous_scale="Reds",
                      title="3+ product customers churn at 86%!")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Active vs Inactive Members")
        active_data = pd.DataFrame({
            "Status": ["Active", "Inactive"],
            "Churn Rate": [14.27, 26.85]
        })
        fig3 = px.bar(active_data, x="Status", y="Churn Rate",
                      color="Status",
                      color_discrete_map={"Active": "#2ecc71", "Inactive": "#e74c3c"},
                      title="Inactive members churn at nearly 2x the rate")
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.subheader("Model Churn Score Distribution")
        fig4 = px.histogram(df, x="churn_probability",
                            color=df["actual_churn"].map({0: "Retained", 1: "Churned"}),
                            nbins=40, barmode="overlay", opacity=0.7,
                            color_discrete_map={"Retained": "#3498db", "Churned": "#e74c3c"},
                            title="Model clearly separates churners from retained customers")
        st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# PAGE 2 — Predict Customer Churn
# ============================================================
elif page == "🔮 Predict Customer Churn":

    st.title("🔮 Customer Churn Predictor")
    st.markdown("Enter customer details to get their churn probability and explanation")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Profile")
        credit_score = st.slider("Credit Score", 300, 850, 650)
        age = st.slider("Age", 18, 92, 40)
        tenure = st.slider("Years with Bank", 0, 10, 3)
        balance = st.number_input("Account Balance ($)", 0, 250000, 75000)

    with col2:
        st.subheader("Account Details")
        num_products = st.selectbox("Number of Products", [1, 2, 3, 4])
        has_cc = st.radio("Has Credit Card?", ["Yes", "No"])
        is_active = st.radio("Active Member?", ["Yes", "No"])
        salary = st.number_input("Estimated Salary ($)", 0, 200000, 80000)
        geography = st.selectbox("Country", ["France", "Germany", "Spain"])
        gender = st.radio("Gender", ["Male", "Female"])

    # Map inputs to model format
    geo_map = {"France": 1, "Germany": 2, "Spain": 3}

    input_data = pd.DataFrame([{
        "CreditScore": credit_score,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": 1 if has_cc == "Yes" else 0,
        "IsActiveMember": 1 if is_active == "Yes" else 0,
        "EstimatedSalary": salary,
        "geography_key": geo_map[geography],
        "Gender": 1 if gender == "Male" else 0
    }])

    if st.button("🔮 Predict Churn Risk", type="primary"):

        prob = model.predict_proba(input_data)[0][1]

        st.markdown("---")
        st.subheader("Prediction Result")

        col_r1, col_r2, col_r3 = st.columns(3)

        # Risk gauge
        if prob < 0.3:
            risk_label = "🟢 LOW RISK"
            color = "green"
        elif prob < 0.6:
            risk_label = "🟡 MEDIUM RISK"
            color = "orange"
        else:
            risk_label = "🔴 HIGH RISK"
            color = "red"

        col_r1.metric("Churn Probability", f"{prob:.1%}")
        col_r2.metric("Risk Level", risk_label)
        col_r3.metric("Retention Priority",
                      "Urgent" if prob > 0.6 else "Monitor" if prob > 0.3 else "Low")

        # SHAP explanation
        st.subheader("Why is this customer at risk?")
        st.markdown("*SHAP values show which factors push the prediction up or down*")

        shap_vals = explainer.shap_values(input_data)
        feature_names = input_data.columns.tolist()

        shap_df = pd.DataFrame({
            "Feature": feature_names,
            "SHAP Value": shap_vals[0],
            "Customer Value": input_data.values[0]
        }).sort_values("SHAP Value", key=abs, ascending=False).head(8)

        shap_df["Impact"] = shap_df["SHAP Value"].apply(
            lambda x: "Increases Churn Risk 🔴" if x > 0 else "Reduces Churn Risk 🟢")

        fig_shap = px.bar(shap_df, x="SHAP Value", y="Feature",
                          orientation="h",
                          color="Impact",
                          color_discrete_map={
                              "Increases Churn Risk 🔴": "#e74c3c",
                              "Reduces Churn Risk 🟢": "#2ecc71"
                          },
                          title="What's driving this customer's churn risk?")
        st.plotly_chart(fig_shap, use_container_width=True)

        # Recommendation
        st.subheader("💡 Recommended Action")
        if prob > 0.6:
            st.error("""
            **Urgent Retention Required**
            - Assign a personal relationship manager
            - Offer a loyalty discount or fee waiver
            - Schedule a proactive check-in call within 7 days
            """)
        elif prob > 0.3:
            st.warning("""
            **Monitor & Engage**
            - Add to email retention campaign
            - Offer relevant product upgrade
            - Check in within 30 days
            """)
        else:
            st.success("""
            **Low Risk — Maintain Relationship**
            - Continue standard engagement
            - Consider cross-sell opportunity
            """)

# ============================================================
# PAGE 3 — Business Impact Simulator
# ============================================================
elif page == "💰 Business Impact Simulator":

    st.title("💰 Retention Business Impact Simulator")
    st.markdown("Simulate the financial impact of your retention strategy")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model Settings")
        threshold = st.slider("Risk Threshold — flag customers above this score",
                              0.1, 0.9, 0.5, 0.05)
        retention_rate = st.slider("Retention success rate (% of flagged saved)",
                                   10, 80, 30)

    with col2:
        st.subheader("Cost Settings")
        cost_per_contact = st.number_input("Cost per retention contact ($)", 5, 200, 50)
        avg_customer_value = st.number_input("Average annual customer value ($)",
                                              100, 5000, 800)

    # Calculations
    flagged = (df["churn_probability"] >= threshold).sum()
    true_churners_flagged = ((df["churn_probability"] >= threshold) &
                              (df["actual_churn"] == 1)).sum()
    false_alarms = flagged - true_churners_flagged

    saved_customers = int(true_churners_flagged * retention_rate / 100)
    revenue_saved = saved_customers * avg_customer_value
    total_cost = flagged * cost_per_contact
    net_benefit = revenue_saved - total_cost
    roi = (net_benefit / total_cost * 100) if total_cost > 0 else 0

    st.markdown("---")
    st.subheader("📊 Simulation Results")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers Flagged", f"{flagged:,}")
    c2.metric("True Churners Caught", f"{true_churners_flagged:,}")
    c3.metric("Customers Saved", f"{saved_customers:,}")
    c4.metric("Net Benefit", f"${net_benefit:,.0f}",
              delta=f"ROI: {roi:.0f}%",
              delta_color="normal" if net_benefit > 0 else "inverse")

    # Threshold sweep chart
    thresholds = np.arange(0.1, 0.9, 0.05)
    results = []
    for t in thresholds:
        f = (df["churn_probability"] >= t).sum()
        tc = ((df["churn_probability"] >= t) & (df["actual_churn"] == 1)).sum()
        sv = int(tc * retention_rate / 100)
        nb = sv * avg_customer_value - f * cost_per_contact
        results.append({"Threshold": round(t, 2), "Net Benefit ($)": nb,
                         "Flagged": f})

    res_df = pd.DataFrame(results)
    fig_roi = px.line(res_df, x="Threshold", y="Net Benefit ($)",
                      title="Net Benefit vs. Risk Threshold",
                      markers=True)
    fig_roi.add_vline(x=threshold, line_dash="dash", line_color="red",
                      annotation_text=f"Current: {threshold}")
    fig_roi.update_layout(yaxis_tickformat="$,.0f")
    st.plotly_chart(fig_roi, use_container_width=True)

    st.markdown("---")
    st.caption("Meridian Bank Churn Analytics | Built with DuckDB, XGBoost, SHAP & Streamlit")
