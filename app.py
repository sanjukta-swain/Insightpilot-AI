import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_cleaning import clean_data

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# Title
# ----------------------------
st.title("📊 InsightPilot AI")
st.subheader("AI-Powered Business Analytics & Decision Intelligence Platform")

st.markdown("---")

# ----------------------------
# File Upload
# ----------------------------
uploaded_file = st.file_uploader(
    "📂 Upload a CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read the file
    if uploaded_file.name.endswith(".csv"):
      try:
       df = pd.read_csv(uploaded_file, encoding="utf-8")
      except UnicodeDecodeError:
       uploaded_file.seek(0)
       df = pd.read_csv(uploaded_file, encoding="latin1")
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File Uploaded Successfully!")
    st.write("columns:")
    st.write(df.columns.tolist())

    # Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    st.markdown("---")

    # Dataset Information
    st.subheader("📊 Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    st.write("### Column Names")
    

    st.write("### Data Types")
    st.dataframe(df.dtypes.astype(str))

    st.markdown("---")

    # Missing Values
    st.subheader("🧹 Missing Values")

    missing = df.isnull().sum()

    st.dataframe(missing)

    # Duplicate Rows
    duplicates = df.duplicated().sum()

    st.write(f"### Duplicate Rows: {duplicates}")
    st.markdown("---")

    st.subheader("🧹 Automatic Data Cleaning")

    cleaned_df, summary = clean_data(df)

    st.success("Dataset cleaned successfully!")
    st.write("### Cleaning Summary")

    st.write(summary)

    st.write("### Cleaned Dataset")

    st.dataframe(cleaned_df)
    st.markdown("---")
    cleaned_df, summary = clean_data(df)

    st.success("Dataset cleaned successfully!")
    st.write("### Cleaning Summary")

    st.write(summary)

    st.write("### Cleaned Dataset")

    st.dataframe(cleaned_df)
    st.markdown("---")

   # ----------------------------
   # Sidebar Filters
   # ----------------------------
    st.sidebar.header("🎛️ Dashboard Filters")

    region = st.sidebar.multiselect(
        "Select Region",
        options=cleaned_df["Region"].unique(),
        default=cleaned_df["Region"].unique()
    )

    category = st.sidebar.multiselect(
        "Select Category",
        options=cleaned_df["Category"].unique(),
        default=cleaned_df["Category"].unique()
    )

    segment = st.sidebar.multiselect(
        "Select Segment",
        options=cleaned_df["Segment"].unique(),
        default=cleaned_df["Segment"].unique()
    )

    filtered_df = cleaned_df[
        (cleaned_df["Region"].isin(region)) &
        (cleaned_df["Category"].isin(category)) &
        (cleaned_df["Segment"].isin(segment))
    ]


    st.subheader("📊 Business Dashboard")
    # Dashboard Metrics

    col1, col2, col3 = st.columns(3)

    with col1:
     st.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.2f}")

    with col2:
     st.metric("💵 Total Profit", f"${filtered_df['Profit'].sum():,.2f}")

    with col3:
     st.metric("📦 Total Orders", filtered_df["Order ID"].nunique())
     st.markdown("---")

    st.subheader("📊 Sales by Region")

    region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
    st.write(cleaned_df.columns.tolist())

    fig = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Region",
    title="Total Sales by Region"
)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("🏆 Top 10 Products by Sales")

    top_products = (
       cleaned_df.groupby("Product Name")["Sales"]
       .sum()
       .sort_values(ascending=False)
       .head(10)
       .reset_index()
    )

    top_products = top_products.sort_values(by="Sales", ascending=True)

    fig = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales",
        title="Top 10 Products by Sales"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🥧 Sales by Category")

    category_sales = (
        cleaned_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales Distribution by Category",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("📈 Monthly Sales Trend")

    cleaned_df["Order Date"] = pd.to_datetime(cleaned_df["Order Date"])

    monthly_sales = (
        cleaned_df.groupby(cleaned_df["Order Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

    fig = px.line(
       monthly_sales,
       x="Order Date",
       y="Sales",
       markers=True,
       title="Monthly Sales Trend"
)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("💵 Profit by Category")

    category_profit = (
        cleaned_df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
   )

    fig = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        color="Category",
        title="Profit by Category"
    ) 

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("🗺️ Sales by State")

    state_sales = (
        cleaned_df.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        state_sales,
        x="State",
        y="Sales",
        color="Sales",
        title="Top 10 States by Sales"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("👥 Top 10 Customers by Sales")

    customer_sales = (
        cleaned_df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        customer_sales,
        x="Sales",
        y="Customer Name",
        orientation="h",
        color="Sales",
        title="Top 10 Customers by Sales"
    )

    st.plotly_chart(fig, use_container_width=True)
