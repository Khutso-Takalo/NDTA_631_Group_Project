import streamlit as st
import pandas as pd
import numpy as np
st.title("Impact of the Informal Economy on Income Inequality in South Africa")

# --- Sidebar: Filters & Theme ---

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="SA Informal Economy & Income Inequality", layout="wide", initial_sidebar_state="expanded")

# Load merged data
data_path = "data/data_processed/merged_clean.csv"
df = pd.read_csv(data_path)

# --- Sidebar Navigation ---
st.sidebar.title("Project Demo Navigation")
section = st.sidebar.radio("Go to Section:", [
    "Project Overview",
    "1. Data Preparation",
    "2. Numerical Analysis",
    "3. Visualization",
    "4. Database Integration",
    "5. Data Analysis",
    "6. Report & Demo"
])

# --- Sidebar Filters ---
st.sidebar.header("Filters & Customization")
year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Select Year Range", min_value=year_min, max_value=year_max, value=(year_min, year_max))
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
indicators = ["Gini_Index", "Informal_Employment"]
selected_indicators = st.sidebar.multiselect("Select Indicators to Plot", indicators, default=indicators)
color_theme = st.sidebar.selectbox("Choose Color Theme", ["Plotly", "Viridis", "Cividis", "Plasma", "Rainbow"])
show_stats = st.sidebar.checkbox("Show Summary Statistics", value=True)

# --- Custom CSS ---
st.markdown("""
<style>
.stApp {background-color: #f7f7fa;}
.block-container {padding-top: 2rem;}
.section-card {background-color:#e3f2fd;padding:1rem;border-radius:10px;margin-bottom:1rem;}
</style>
""", unsafe_allow_html=True)

# --- Section: Project Overview ---
if section == "Project Overview":
    st.title("NDTA 631 Group Assignment Demo Dashboard")
    st.markdown("""
    <div class='section-card'>
    <b>Module:</b> Data Analysis And Visualization<br>
    <b>Assignment:</b> Group Data Analysis & Visualization Pipeline<br>
    <b>Goal:</b> Explore how the informal economy affects income inequality in South Africa using World Bank datasets.<br>
    <b>Deliverables:</b> Data Preparation, Numerical Analysis, Visualization, Database Integration, Data Analysis, Report & Demo.<br>
    <b>Group Size:</b> 6-7 students<br>
    <b>Due Date:</b> 4 September 2025<br>
    </div>
    """, unsafe_allow_html=True)
    st.success("Use the sidebar to navigate through each deliverable and interact with the data.")

# --- Section 1: Data Preparation ---
elif section == "1. Data Preparation":
    st.header("1. Data Preparation")
    st.markdown("""
    <div class='section-card'>
    <b>Tasks:</b> Load, clean, and prepare two real datasets. Handle missing values, generate descriptive stats and insights.<br>
    <b>Tools:</b> Python, Pandas<br>
    </div>
    """, unsafe_allow_html=True)
    st.write("Preview of merged dataset:")
    st.dataframe(df_filtered.head(10), use_container_width=True)
    # Show raw data sample
    st.subheader("Raw Data Sample (Income & Informal)")
    try:
        raw_income = pd.read_csv("data/data_raw/OECD_IDD.csv").head(5)
        raw_informal = pd.read_csv("data/data_raw/WB_INFECDB.csv").head(5)
        st.write("Income raw sample:")
        st.dataframe(raw_income)
        st.write("Informal raw sample:")
        st.dataframe(raw_informal)
    except Exception as e:
        st.warning(f"Raw data files not found or could not be loaded: {e}")
    # Show missing values
    st.subheader("Missing Values in Merged Data")
    st.write(df_filtered.isna().sum())
    # Show column names
    st.subheader("Column Names")
    st.write(list(df_filtered.columns))
    if show_stats:
        st.subheader("Summary Statistics")
        st.write(df_filtered.describe())
    st.info("See notebook 01_data_preparation.ipynb for full code and cleaning steps.")

# --- Section 2: Numerical Analysis ---
elif section == "2. Numerical Analysis":
    st.header("2. Numerical Analysis")
    st.markdown("""
    <div class='section-card'>
    <b>Tasks:</b> Use NumPy for calculations, reshape arrays, perform operations, explain findings.<br>
    <b>Tools:</b> Python, NumPy<br>
    </div>
    """, unsafe_allow_html=True)
    st.write("Numerical analysis results (see notebook 02_numerical_analysis.ipynb for details):")
    # Summary statistics
    st.subheader("Summary Statistics (Mean, Median, Std, Min, Max)")
    summary = df_filtered[["Gini_Index", "Informal_Employment"]].describe().T
    summary["median"] = df_filtered[["Gini_Index", "Informal_Employment"]].median()
    st.write(summary)
    # Show NumPy array operations
    st.subheader("NumPy Array Operations")
    arr_gini = df_filtered["Gini_Index"].to_numpy()
    arr_informal = df_filtered["Informal_Employment"].to_numpy()
    st.write("Gini Index array shape:", arr_gini.shape)
    st.write("Informal Employment array shape:", arr_informal.shape)
    st.write("Gini Index (first 5):", arr_gini[:5])
    st.write("Informal Employment (first 5):", arr_informal[:5])
    # Example: Calculate mean difference
    mean_diff = np.mean(arr_gini - arr_informal)
    st.metric("Mean Difference (Gini - Informal)", f"{mean_diff:.2f}")
    # Example: Correlation
    corr = df_filtered["Informal_Employment"].corr(df_filtered["Gini_Index"])
    st.metric("Correlation (Informal Employment vs. Gini Index)", f"{corr:.3f}")

# --- Section 3: Visualization ---
elif section == "3. Visualization":
    st.header("3. Visualization")
    st.markdown("""
    <div class='section-card'>
    <b>Tasks:</b> Create clear plots (bar, scatter, box, histograms), explain trends and patterns, use color and labels.<br>
    <b>Tools:</b> Python, Matplotlib, Plotly<br>
    </div>
    """, unsafe_allow_html=True)
    # Bar Plot: Average Gini Index and Informal Employment
    st.subheader("Bar Plot: Average Gini Index vs Informal Employment")
    avg_gini = df_filtered["Gini_Index"].mean()
    avg_informal = df_filtered["Informal_Employment"].mean()
    fig_bar = px.bar(x=["Gini Index", "Informal Employment"], y=[avg_gini, avg_informal], color=["Gini Index", "Informal Employment"],
        color_discrete_map={"Gini Index": "#1f77b4", "Informal Employment": "#ff7f0e"}, title="Average Gini Index vs Informal Employment")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Histograms
    st.subheader("Histogram: Distribution of Indicators")
    fig_hist = px.histogram(df_filtered, x="Gini_Index", nbins=10, color_discrete_sequence=["#1f77b4"], title="Gini Index Distribution")
    st.plotly_chart(fig_hist, use_container_width=True)
    fig_hist2 = px.histogram(df_filtered, x="Informal_Employment", nbins=10, color_discrete_sequence=["#ff7f0e"], title="Informal Employment Distribution")
    st.plotly_chart(fig_hist2, use_container_width=True)

    # Box Plot
    st.subheader("Box Plot: Spread and Outliers")
    fig_box = px.box(df_filtered, y=["Gini_Index", "Informal_Employment"], color_discrete_sequence=["#1f77b4", "#ff7f0e"], title="Boxplot of Gini Index and Informal Employment")
    st.plotly_chart(fig_box, use_container_width=True)

    # Scatter Plot
    st.subheader("Scatter Plot: Relationship Between Indicators")
    corr = df_filtered["Informal_Employment"].corr(df_filtered["Gini_Index"])
    colorscale_map = {
        "Plotly": "plotly3",
        "Viridis": "viridis",
        "Cividis": "cividis",
        "Plasma": "plasma",
        "Rainbow": "rainbow"
    }
    scatter_colorscale = colorscale_map.get(color_theme, "plotly3")
    fig_scatter = px.scatter(
        df_filtered,
        x="Informal_Employment",
        y="Gini_Index",
        trendline="ols",
        color="Year",
        color_continuous_scale=scatter_colorscale,
        title="Scatter Plot: Informal Employment vs. Gini Index"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.metric("Correlation coefficient", f"{corr:.3f}")

    # Line Plot: Trends Over Time
    st.subheader("Line Plot: Trends Over Time")
    fig_trend = px.line(
        df_filtered,
        x="Year",
        y=["Gini_Index", "Informal_Employment"],
        labels={"value": "Value", "variable": "Indicator"},
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        title="Income Inequality and Informal Employment Over Time"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.info("See notebook 03_visualization.ipynb for more visualizations and code.")

# --- Section 4: Database Integration ---
elif section == "4. Database Integration":
    st.header("4. Database Integration")
    st.markdown("""
    <div class='section-card'>
    <b>Tasks:</b> Build and query a database, update/delete records, load database data into Pandas.<br>
    <b>Tools:</b> Python, SQLite, Pandas<br>
    </div>
    """, unsafe_allow_html=True)
    st.info("Database operations and integration steps are shown in notebook 04_database_integration.ipynb.")
    st.write("Sample of merged data loaded from database:")
    st.dataframe(df_filtered.head(10), use_container_width=True)
    st.markdown("""
    <b>Database Operations:</b><br>
    - <span style='color:green'>Create Table:</span> Stores year, Gini Index, Informal Employment.<br>
    - <span style='color:blue'>Insert Data:</span> Loads CSV and inserts records.<br>
    - <span style='color:orange'>Query:</span> Selects all records for analysis.<br>
    - <span style='color:purple'>Update:</span> Safely updates Gini Index for a year.<br>
    - <span style='color:red'>Delete:</span> Removes records for a year.<br>
    - <span style='color:teal'>Load to Pandas:</span> Enables further analysis and visualization.<br>
    """, unsafe_allow_html=True)

# --- Section 5: Data Analysis ---
elif section == "5. Data Analysis":
    st.header("5. Data Analysis")
    st.markdown("""
    <div class='section-card'>
    <b>Tasks:</b> Clean and transform data, apply conditional formatting, create charts, summarize findings.<br>
    <b>Tools:</b> Python, Pandas, Matplotlib, Excel<br>
    </div>
    """, unsafe_allow_html=True)
    # Data Cleaning: Remove outliers, fill missing values, create new columns
    st.subheader("Data Cleaning and Transformation")
    Q1 = df_filtered[["Gini_Index", "Informal_Employment"]].quantile(0.25)
    Q3 = df_filtered[["Gini_Index", "Informal_Employment"]].quantile(0.75)
    IQR = Q3 - Q1
    df_clean = df_filtered[~((df_filtered[["Gini_Index", "Informal_Employment"]] < (Q1 - 1.5 * IQR)) | (df_filtered[["Gini_Index", "Informal_Employment"]] > (Q3 + 1.5 * IQR))).any(axis=1)]
    df_clean = df_clean.fillna(df_clean.mean())
    df_clean["Gini_Informal_Ratio"] = df_clean["Gini_Index"] / df_clean["Informal_Employment"]
    st.write(df_clean.head())

    # Conditional Formatting: Highlight High Inequality
    st.subheader("Conditional Formatting: Highlight High Inequality")
    high_gini = df_clean["Gini_Index"] > df_clean["Gini_Index"].quantile(0.75)
    df_highlight = df_clean.copy()
    df_highlight["Highlight"] = ["High" if x else "Normal" for x in high_gini]
    st.write(df_highlight[["Year", "Gini_Index", "Highlight"]].head(10))

    # Chart: Highlighted Gini Index Over Time
    st.subheader("Chart: Gini Index Over Time (High Inequality Highlighted)")
    import plotly.graph_objects as go
    colors = ["red" if h == "High" else "blue" for h in df_highlight["Highlight"]]
    fig_highlight = go.Figure()
    fig_highlight.add_trace(go.Bar(x=df_highlight["Year"], y=df_highlight["Gini_Index"], marker_color=colors))
    fig_highlight.update_layout(title="Gini Index Over Time (High Inequality Highlighted)", xaxis_title="Year", yaxis_title="Gini Index")
    st.plotly_chart(fig_highlight, use_container_width=True)

    # Chart: Gini/Informal Ratio Over Time
    st.subheader("Chart: Gini/Informal Ratio Over Time")
    fig_ratio = px.line(df_clean, x="Year", y="Gini_Informal_Ratio", color_discrete_sequence=["green"], title="Gini Index to Informal Employment Ratio Over Time")
    st.plotly_chart(fig_ratio, use_container_width=True)

    # Summary of Findings
    st.subheader("Summary of Findings")
    st.markdown("""
    - Data cleaning removed outliers and filled missing values, improving reliability.<br>
    - Conditional formatting highlighted years with high inequality, making patterns easy to spot.<br>
    - Charts revealed trends in both absolute and relative inequality over time.<br>
    <br>
    **Conclusion:**<br>
    Python enables robust data analysis, visualization, and pattern recognition, supporting deeper insights into income inequality and informal employment in South Africa.
    """, unsafe_allow_html=True)
    st.info("See notebook 05_data_analysis.ipynb for full analysis and charts.")

# --- Section 6: Report & Demo ---
elif section == "6. Report & Demo":
    st.header("6. Report & Demo")
    st.markdown("""
    <div class='section-card'>
    <b>Tasks:</b> Write a 7–9 page report, include dataset details, methods, visualisations, and conclusions. Present with clear demo.<br>
    <b>Tools:</b> Word, PDF, Streamlit, GitHub<br>
    </div>
    """, unsafe_allow_html=True)
    st.success("Download the full report and demo video from the GitHub repository.")
    st.write("Project execution instructions, environment configuration, and codebase are available in the repo.")
