import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────
# Page configuration
st.set_page_config(page_title="Sri Lanka Labor & Social Protection Dashboard", layout="centered")

# ────────────────────────────────────────────────
# Load the cleaned data
df = pd.read_csv(r"C:\Users\Lenovo\Desktop\Nethmi\Data Science\DSPL_Individual\cleaned_data.csv")

# ────────────────────────────────────────────────
# Sidebar filters
st.sidebar.title("🔍 Filter Options")
chart_type = st.sidebar.radio("Select Chart Type", ["Line Chart", "Bar Chart"])

# ────────────────────────────────────────────────
# Indicator groups
indicators = {
    "Unemployment & Labor Participation": [
        "Unemployment, total (% of total labor force) (modeled ILO estimate)",
        "Labor force participation rate, total (% of total population ages 15+) (modeled ILO estimate)"
    ],
    "Employment by Sector": [
        "Employment in agriculture (% of total employment) (modeled ILO estimate)",
        "Employment in industry (% of total employment) (modeled ILO estimate)",
        "Employment in services (% of total employment) (modeled ILO estimate)"
    ],
    "Social Protection Coverage": [
        "Coverage of social protection and labor programs (% of population)",
        "Coverage in extreme poor (<$2.15 a day) (%) -All Social Protection and Labor",
        "Coverage (%) -All Social Protection and Labor -rural",
        "Coverage (%) -All Social Protection and Labor -urban"
    ],
    "Poverty Reduction Impact": [
        "Poverty Gap reduction (%) - All Social Protection and Labor -1st quintile (poorest)",
        "Poverty Headcount reduction (%) - All Social Protection and Labor -1st quintile (poorest)",
        "Gini inequality index reduction (%) - All Social Protection and Labor"
    ]
}

# Indicator descriptions
indicator_descriptions = {
    "Unemployment, total (% of total labor force) (modeled ILO estimate)":
        "This shows the share of the labor force that is unemployed, based on ILO modeling.",
    "Labor force participation rate, total (% of total population ages 15+) (modeled ILO estimate)":
        "This represents the percentage of the working-age population (15+) that is actively working or seeking work.",
    "Employment in agriculture (% of total employment) (modeled ILO estimate)":
        "This measures the proportion of employed people working in the agriculture sector.",
    "Employment in industry (% of total employment) (modeled ILO estimate)":
        "This indicates the share of jobs in the industrial sector, including manufacturing and construction.",
    "Employment in services (% of total employment) (modeled ILO estimate)":
        "This shows the portion of the workforce employed in services such as retail, finance, and education.",
    "Coverage of social protection and labor programs (% of population)":
        "This shows the percentage of the population covered by at least one social protection or labor program.",
    "Coverage in extreme poor (<$2.15 a day) (%) -All Social Protection and Labor":
        "This shows what percentage of people living below $2.15/day are covered by social protection programs.",
    "Coverage (%) -All Social Protection and Labor -rural":
        "This represents social protection coverage for people in rural areas.",
    "Coverage (%) -All Social Protection and Labor -urban":
        "This represents social protection coverage for people in urban areas.",
    "Poverty Gap reduction (%) - All Social Protection and Labor -1st quintile (poorest)":
        "This measures the poverty gap reduction for the bottom 20% of the income distribution — the 'poorest' quintile in the country.",
    "Poverty Headcount reduction (%) - All Social Protection and Labor -1st quintile (poorest)":
        "This shows how social protection programs reduce the number of people living in poverty (headcount) in the poorest 20%.",
    "Gini inequality index reduction (%) - All Social Protection and Labor":
        "This shows how much social protection programs reduce income inequality, using the Gini index."
}

# ────────────────────────────────────────────────
# Section and Indicator selection
section = st.sidebar.selectbox("Select Insight Area", ["Choose an option"] + list(indicators.keys()), index=0)
indicator = ""
indicator_options = []

if section != "Choose an option":
    indicator_options = indicators[section]

indicator = st.sidebar.selectbox("Choose an Indicator", ["Choose an option"] + sorted(indicator_options) if indicator_options else ["Choose an option"], index=0)

# ────────────────────────────────────────────────
# Title and Dashboard Description
st.title("🇱🇰 Sri Lanka Labor & Social Protection Indicators Dashboard")
st.markdown("""
This dashboard presents key indicators related to labor market trends, unemployment, social protection coverage, and poverty reduction in Sri Lanka. Use the filters to explore different dimensions of the data.
""")

# Show sample visuals only if no selection is made
if section == "Choose an option" or indicator == "Choose an option":
    # Group 1: Unemployment & Labor Participation
    st.markdown("### 👷 Unemployment & Labor Participation")
    group1_df = df[df["Indicator Name"].isin(indicators["Unemployment & Labor Participation"])]
    fig1 = px.line(group1_df, x="Year", y="Value", color="Indicator Name", title="Unemployment & Participation Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    # Group 2: Employment by Sector
    st.markdown("### 🏭 Employment by Sector")
    avg_df = df[df["Indicator Name"].isin(indicators["Employment by Sector"])]
    avg_df = avg_df.groupby("Indicator Name")["Value"].mean().reset_index()
    fig_pie = px.pie(avg_df, names="Indicator Name", values="Value", title="Average Employment Share by Sector")
    st.plotly_chart(fig_pie, use_container_width=True)

    trend_df = df[df["Indicator Name"].isin(indicators["Employment by Sector"])]
    fig_line = px.line(trend_df, x="Year", y="Value", color="Indicator Name", title="Employment Trends by Sector Over Time")
    st.plotly_chart(fig_line, use_container_width=True)

    # Group 3: Social Protection Coverage
    st.markdown("### 🛡️ Social Protection Coverage")
    group3_df = df[df["Indicator Name"].isin(indicators["Social Protection Coverage"])]
    fig3 = px.line(group3_df, x="Year", y="Value", color="Indicator Name", title="Social Protection Coverage by Type")
    st.plotly_chart(fig3, use_container_width=True)

    # Group 4: Poverty Reduction Impact
    st.markdown("### 📉 Poverty Reduction Impact")
    group4_df = df[df["Indicator Name"].isin(indicators["Poverty Reduction Impact"])]
    fig4 = px.line(group4_df, x="Year", y="Value", color="Indicator Name", title="Poverty Impact Indicators")
    st.plotly_chart(fig4, use_container_width=True)

else:
    # ────────────────────────────────────────────────
    # Filter data and show user-selected content
    filtered_df = df[df["Indicator Name"] == indicator].copy()
    filtered_df = filtered_df.sort_values("Year")

    # Add year range slider after data is filtered
    years = sorted(filtered_df["Year"].unique())
    min_year, max_year = int(min(years)), int(max(years))
    year_range = st.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year), step=1)

    # Apply year filter to the data
    filtered_df = filtered_df[(filtered_df["Year"] >= year_range[0]) & (filtered_df["Year"] <= year_range[1])]

    # Chart and Description
    st.subheader(f"📈 {indicator} Over Time")
    description = indicator_descriptions.get(indicator.strip(), "ℹ️ No description available for this indicator.")
    st.markdown(f"📝 {description}")

    if chart_type == "Line Chart":
        fig = px.line(filtered_df, x="Year", y="Value", markers=True, title=indicator)
    else:
        fig = px.bar(filtered_df, x="Year", y="Value", color="Year", title=indicator)

    fig.update_layout(title_x=0.5, xaxis_title="Year", yaxis_title="Value")
    st.plotly_chart(fig, use_container_width=True)

    # Key Stats
    st.markdown("### 📊 Key Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average", f"{filtered_df['Value'].mean():.2f}")
    col2.metric("Max", f"{filtered_df['Value'].max():.2f}")
    col3.metric("Min", f"{filtered_df['Value'].min():.2f}")

    # Data Table and Download
    st.markdown("### 📋 Data Preview")
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"{indicator.replace(' ', '_')}_SriLanka.csv",
        mime='text/csv'
    )
    
# Footer
st.caption("📊 Data Source: World Bank via Humanitarian Data Exchange (HDX)")

