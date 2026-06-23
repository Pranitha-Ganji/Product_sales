import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Product Sales Dashboard", layout="wide")
st.title("📊 Product Sales Insights Dashboard")

# 2. Database Connection Function
@st.cache_data # Keeps the app fast by caching the data
def fetch_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Default XAMPP username
        password="dbms26",         # Default XAMPP password is empty
        database="mysql"     # Based on your phpMyAdmin screen, your data is in 'mysql'
    )
    query = "SELECT * FROM product_sales;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch the data
try:
    df = fetch_data()
    
    # 3. Key Metrics (KPIs)
    total_revenue = df['revenue'].sum()
    total_units = df['units_sold'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    with col2:
        st.metric(label="Total Units Sold", value=f"{total_units:,}")
        
    st.markdown("---")

    # 4. Visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Revenue by Product")
        fig_bar = px.bar(df, x='product_name', y='revenue', color='category', 
                         labels={'product_name': 'Product', 'revenue': 'Revenue ($)'},
                         template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col4:
        st.subheader("Market Share by Category")
        fig_pie = px.pie(df, values='revenue', names='category', hole=0.4,
                         template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)

    # 5. Raw Data Table Toggle
    with st.expander("View Raw Data Frame"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.info("Make sure XAMPP (Apache & MySQL) is running and the database details match!")