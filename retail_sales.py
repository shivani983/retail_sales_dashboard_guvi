import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("🛍️ Adidas Sales Dashboard")

# Load & preprocess data
df1 = pd.read_csv('Adidas Sales.csv')

# Cleaning
df1.drop(columns=['Total Sales'], inplace=True)
df1['Price per Unit'] = pd.to_numeric(df1['Price per Unit'].replace('[\$,]', '', regex=True), errors='coerce').astype('Int64')
df1['Units Sold'] = df1['Units Sold'].replace(',', '', regex=True).astype(float).astype(int)
df1['total_sales'] = df1['Price per Unit'] * df1['Units Sold']
df1['Operating Profit'] = df1['Operating Profit'].replace('[\$,]', '', regex=True).astype(float)
df1['Invoice Date'] = pd.to_datetime(df1['Invoice Date'])
df1['YearMonth'] = df1['Invoice Date'].dt.to_period('M').astype(str)

# KPI Metrics
total_revenue = df1['total_sales'].sum()
units_sold = df1['Units Sold'].sum()
avg_order_value = total_revenue / units_sold

# Sidebar
chart_type = st.sidebar.radio("📊 Select Visualization", 
                              ["📄 Show Dataset", "📌 KPI Metrics", "📍 Bar Chart: Sales by Region", 
                               "📈 Line Chart: Monthly Sales Trend", 
                               "🥧 Pie Chart: Product Revenue Share"])

# Show dataset
if chart_type == "📄 Show Dataset":
    st.subheader("🧾 Raw Sales Data")
    st.dataframe(df1)

# KPI Metrics
elif chart_type == "📌 KPI Metrics":
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("📦 Units Sold", f"{units_sold:,}")
    col3.metric("📈 Avg. Order Value", f"${avg_order_value:.2f}")

# Bar Chart
elif chart_type == "📍 Bar Chart: Sales by Region":
    st.subheader("📍 Total Sales by Region")
    region_sales = df1.groupby('Region')['total_sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    region_sales.plot(kind='bar', color='mediumseagreen', ax=ax)
    ax.set_title("Total Sales by Region", fontsize=14)
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Sales (USD)")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Line Chart
elif chart_type == "📈 Line Chart: Monthly Sales Trend":
    st.subheader("📈 Monthly Sales Trend")
    monthly_sales = df1.groupby('YearMonth')['total_sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_sales['YearMonth'], monthly_sales['total_sales'], 
            marker='o', linestyle='-', color='darkgreen')
    ax.set_title("Monthly Sales Trend", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales (USD)")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Pie Chart
elif chart_type == "🥧 Pie Chart: Product Revenue Share":
    st.subheader("🥧 Product Category Share in Total Revenue")
    category_sales = df1.groupby('Product')['total_sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = plt.cm.Greens(range(100, 100 + len(category_sales)*20, 20))
    ax.pie(category_sales['total_sales'], 
           labels=category_sales['Product'], 
           autopct='%1.1f%%', 
           startangle=140, 
           colors=colors,
           wedgeprops={'edgecolor': 'white'})
    ax.set_title('Product Category Share in Total Revenue', fontsize=14, fontweight='bold')
    st.pyplot(fig)
