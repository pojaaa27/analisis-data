"""
TokoKita Dashboard - Live Coding Demo
Dashboard ini mendemonstrasikan cara membuat dashboard Streamlit
untuk proyek analisis data Dicoding
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="TokoKita Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    main_df = pd.read_csv('main_data.csv')
    rfm_df = pd.read_csv('rfm_data.csv')
    customer_geo = pd.read_csv('customer_geo.csv')
    seller_geo = pd.read_csv('seller_geo.csv')
    
    main_df['order_date'] = pd.to_datetime(main_df['order_date'])
    return main_df, rfm_df, customer_geo, seller_geo

main_df, rfm_df, customer_geo, seller_geo = load_data()

# ============================================
# SIDEBAR
# ============================================
st.sidebar.title("🛒 TokoKita Dashboard")
st.sidebar.markdown("---")

# Date Filters
min_date = main_df['order_date'].min().date()
max_date = main_df['order_date'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Filter data
filtered_df = main_df[
    (main_df['order_date'].dt.date >= start_date) &
    (main_df['order_date'].dt.date <= end_date)
]



st.sidebar.markdown("---")


# ============================================
# MAIN CONTENT
# ============================================
st.title("📊 TokoKita Analytics Dashboard")
st.markdown("Dashboard analisis penjualan dan pelanggan TokoKita")

# ============================================
# METRICS ROW
# ============================================
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_orders = filtered_df['order_id'].nunique()
    st.metric("Total Orders", f"{total_orders:,}")

with col2:
    total_revenue = filtered_df['total_price'].sum()
    st.metric("Total Revenue", f"Rp {total_revenue:,.0f}")

with col3:
    total_customers = filtered_df['customer_id'].nunique()
    st.metric("Total Customers", f"{total_customers:,}")

with col4:
    avg_order = total_revenue / total_orders if total_orders > 0 else 0
    st.metric("Avg Order Value", f"Rp {avg_order:,.0f}")

# ============================================
# MONTHLY TREND
# ============================================
st.markdown("---")
st.subheader("📈 Monthly Revenue Trend")

monthly = filtered_df.groupby(filtered_df['order_date'].dt.to_period('M')).agg({
    'total_price': 'sum'
}).reset_index()
monthly['order_date'] = monthly['order_date'].astype(str)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(monthly['order_date'], monthly['total_price'], marker='o', linewidth=2, color='#1f77b4')
ax.fill_between(monthly['order_date'], monthly['total_price'], alpha=0.3)
ax.set_xlabel('Month')
ax.set_ylabel('Revenue (Rp)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rp {x/1e6:.1f}M'))
plt.xticks(rotation=45)
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close()

# ============================================
# PRODUCT CATEGORIES
# ============================================
st.markdown("---")
st.subheader("🏆 Top Product Categories")
category_sales = filtered_df.groupby('category')['total_price'].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(12, 6))
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(category_sales)))
ax.barh(category_sales.index, category_sales.values, color=colors)
ax.set_xlabel('Revenue (Rp)')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
st.pyplot(fig)
plt.close()


# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("**This Dashboard is created by Muhammad Fauza**")
st.markdown("              2026                  ")