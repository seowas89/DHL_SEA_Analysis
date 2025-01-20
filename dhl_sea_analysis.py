import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("DHL SEA Campaign Analysis Dashboard")
st.markdown("**Confidential SEA Campaign Data Analysis**")

# File upload section
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    # Load data
    data = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview:")
    st.dataframe(data.head())

    # Example metrics: Click-Through Rate (CTR), Cost Per Click (CPC), Conversion Rate
    st.write("### Key Metrics Calculation")

    # Ensure required columns exist
    required_columns = ['Market', 'Clicks', 'Impressions', 'Cost', 'Conversions']
    if all(col in data.columns for col in required_columns):
        data['CTR'] = (data['Clicks'] / data['Impressions']) * 100
        data['CPC'] = data['Cost'] / data['Clicks']
        data['Conversion Rate'] = (data['Conversions'] / data['Clicks']) * 100

        # Display calculated metrics
        st.write("#### Metrics Summary")
        metrics_summary = data.groupby('Market')[['CTR', 'CPC', 'Conversion Rate']].mean().reset_index()
        st.dataframe(metrics_summary)

        # Visualizations
        st.write("### Visualizations")

        # CTR Visualization
        st.write("#### Click-Through Rate (CTR) by Market")
        plt.figure(figsize=(10, 5))
        sns.barplot(data=metrics_summary, x='Market', y='CTR', palette="viridis")
        plt.title("CTR by Market")
        plt.ylabel("CTR (%)")
        plt.xlabel("Market")
        st.pyplot(plt)

        # CPC Visualization
        st.write("#### Cost Per Click (CPC) by Market")
        plt.figure(figsize=(10, 5))
        sns.barplot(data=metrics_summary, x='Market', y='CPC', palette="magma")
        plt.title("CPC by Market")
        plt.ylabel("CPC (Cost per Click)")
        plt.xlabel("Market")
        st.pyplot(plt)

        # Conversion Rate Visualization
        st.write("#### Conversion Rate by Market")
        plt.figure(figsize=(10, 5))
        sns.barplot(data=metrics_summary, x='Market', y='Conversion Rate', palette="cool")
        plt.title("Conversion Rate by Market")
        plt.ylabel("Conversion Rate (%)")
        plt.xlabel("Market")
        st.pyplot(plt)

        # Suggestions for budget re-allocation
        st.write("### Budget Re-Allocation Suggestions")
        top_performers = metrics_summary.sort_values(by='Conversion Rate', ascending=False).head(3)
        st.write("#### Top Performing Markets Based on Conversion Rate")
        st.dataframe(top_performers)

        st.markdown(
            "Based on the analysis, we recommend reallocating the budget as follows:")
        st.markdown(
            "1. Increase the budget for high-performing markets with high conversion rates and low CPC (e.g., {}).")
        st.markdown(
            "2. Reduce the budget for underperforming markets with low CTR and high CPC.")
        st.markdown(
            "3. Continuously monitor these metrics to adjust allocations dynamically.")

    else:
        st.error(f"Missing required columns in the uploaded file. Ensure the file contains: {', '.join(required_columns)}")
