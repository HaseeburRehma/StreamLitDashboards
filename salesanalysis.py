import pandas as pd 
import streamlit as st
import plotly.express as px
import base64

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("surveyimg.png")

page_bg_img = f"""
<style>
body {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: cover;
}}
.stSidebar {{ 
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
.stMarkdown {{
color: white;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.header('Survey Results 2024')
st.subheader('Company Sales Survey Annual Report')

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----

company_logo = "logo.jpg"

# Display company logo and name in the sidebar
st.sidebar.image(company_logo, use_column_width=True)
st.sidebar.title("ENCS Networks")

# Add some space between the logo and other sidebar content
st.sidebar.markdown("---")

st.sidebar.header("Select the Filters you want to Apply:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

# Display KPIs in a row layout
kpi_columns = st.columns(3)
with kpi_columns[0]:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")

with kpi_columns[1]:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

with kpi_columns[2]:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {':star:' * int(round(average_rating, 1))}")
    

# sales by productline

sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales= px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation= "h",
    title="<b> Sales By Product Line </b>",
    color_discrete_sequence=["#0083B8"] * len (sales_by_product_line),
    template="plotly_white"
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis= (dict(showgrid=False))
)

# sales By Hour 

sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title= "<b> Sales By Total Hours </b>",
    color_discrete_sequence=["#0083B8"] * len (sales_by_hour),
    template= "plotly_white"
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor= "rgba(0,0,0,0)",
    yaxis= (dict(showgrid=False))
)

kpi_columns = st.columns(2)  
with kpi_columns[0]:
    st.plotly_chart(fig_hourly_sales, use_container_width=True)
with kpi_columns[1]:
    st.plotly_chart(fig_product_sales, use_container_width=True)


# Sales by City
sales_by_city = df_selection.groupby(by=["City"])[["Total"]].sum().sort_values(by="Total")
fig_sales_by_city = px.bar(
    sales_by_city,
    x=sales_by_city.index,
    y="Total",
    title="<b> Sales By City </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_city),
    template="plotly_white"
)
fig_sales_by_city.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(title="Total Sales")
)

# Sales by Customer Type
sales_by_customer_type = df_selection["Customer_type"].value_counts()
fig_sales_by_customer_type = px.pie(
    sales_by_customer_type,
    values=sales_by_customer_type.values,
    names=sales_by_customer_type.index,
    title="<b> Sales By Customer Type </b>",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig_sales_by_customer_type.update_traces(textposition='inside', textinfo='percent+label')

# Display additional graphs
additional_columns = st.columns(2)
with additional_columns[0]:
    st.plotly_chart(fig_sales_by_city, use_container_width=True)
with additional_columns[1]:
    st.plotly_chart(fig_sales_by_customer_type, use_container_width=True)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
