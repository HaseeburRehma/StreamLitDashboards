import streamlit as st
import pandas as pd
import plotly.express as px
import hydralit_components as hc
import seaborn as sns
import matplotlib.pyplot as plt
import time

st.sidebar.title("IBM HR ANALYTICS.Inc")


# your dashboard content here
df = pd.read_excel("IBMHR.xlsx")
# can apply customisation to almost all the properties of the progress bar
override_theme_1 = {'bgcolor': '#EFF8F7', 'progress_color': 'green'}
override_theme_2 = {'bgcolor': 'green', 'content_color': 'white', 'progress_color': 'red'}
override_theme_3 = {'content_color': 'red', 'progress_color': 'orange'}
# for 3 loaders from the standard loader group
loader_delay = 3
with hc.HyLoader('Now doing loading', hc.Loaders.standard_loaders, index=[3, 0, 5]):
    time.sleep(loader_delay)
# Adding Snow Animation
# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Load Animation
animation_symbol = "❄"

st.markdown(
    f"""
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    """,
    unsafe_allow_html=True,
    )
# Create for Department
department = st.sidebar.multiselect("Pick Departments", df["Department"].unique())
if not department:
    df2 = df.copy()
else:
    df2 = df[df["Department"].isin(department)]

# Create for Education Level
education_level = st.sidebar.multiselect("Pick Education Levels", df["Education"].unique())
if not education_level:
    df3 = df2.copy()
else:
    df3 = df2[df2["Education"].isin(education_level)]

# Create for Job Role
job_role = st.sidebar.multiselect("Pick Job Roles", df3["JobRole"].unique())
if not job_role:
    df4 = df3.copy()
else:
    df4 = df3[df3["JobRole"].isin(job_role)]

# Create for Environment Satisfaction
environment_satisfaction = st.sidebar.multiselect("Pick Environment Satisfaction Levels", df4["EnvironmentSatisfaction"].unique())
if not environment_satisfaction:
    df5 = df4.copy()
else:
    df5 = df4[df4["EnvironmentSatisfaction"].isin(environment_satisfaction)]

# Create for Job Involvement
job_involvement = st.sidebar.multiselect("Pick Job Involvement Levels", df5["JobInvolvement"].unique())
if not job_involvement:
    df6 = df5.copy()
else:
    df6 = df5[df5["JobInvolvement"].isin(job_involvement)]

# Create for Job Satisfaction
job_satisfaction = st.sidebar.multiselect("Pick Job Satisfaction Levels", df6["JobSatisfaction"].unique())
if not job_satisfaction:
    df7 = df6.copy()
else:
    df7 = df6[df6["JobSatisfaction"].isin(job_satisfaction)]

# Filtered DataFrame
filtered_df = df7

# Employee attrition breakdown by job role and distance from home
st.subheader("Employee Attrition Breakdown")
attrition_breakdown = px.histogram(filtered_df, x="DistanceFromHome", color="JobRole", facet_col="Attrition", 
                                   labels={"DistanceFromHome": "Distance from Home"})
st.plotly_chart(attrition_breakdown)


# Employee bar plot based on Job Satisfaction level
st.subheader("Bar Plot based on Job Satisfaction Level")
job_satisfaction_bar_plot = px.bar(filtered_df["JobSatisfaction"].value_counts().reset_index(), x="index", y="JobSatisfaction",
                                   labels={"index": "Job Satisfaction Level", "JobSatisfaction": "Count"},
                                   title="Job Satisfaction Level Distribution",
                                   template="plotly")
st.plotly_chart(job_satisfaction_bar_plot)

# Average monthly income by education and attrition
st.subheader("Average Monthly Income by Education and Attrition")
income_by_education_attrition = filtered_df.groupby(["Education", "Attrition"])["MonthlyIncome"].mean().reset_index()
income_chart = px.bar(income_by_education_attrition, x="Education", y="MonthlyIncome", color="Attrition",
                      labels={"Education": "Education Level", "MonthlyIncome": "Average Monthly Income"},
                      title="Average Monthly Income by Education and Attrition")
st.plotly_chart(income_chart)

# Employee pie chart for Department distribution
st.subheader("Department Distribution")
department_pie_chart = px.pie(filtered_df["Department"].value_counts().reset_index(), names="index", values="Department",
                              hole=0.1,title="Department Distribution",
                              template="plotly")
st.plotly_chart(department_pie_chart)

# employee pie chart for Job Role distribution
st.subheader("Job Role Distribution")
job_role_pie_chart = px.pie(filtered_df["JobRole"].value_counts().reset_index(), names="index", values="JobRole",
                            hole=0.1, title="Job Role Distribution",
                            template="plotly")
st.plotly_chart(job_role_pie_chart)

# Employee histogram for Monthly Income
st.subheader("Histogram for Monthly Income")
monthly_income_histogram = px.histogram(filtered_df, x="MonthlyIncome", title="Monthly Income Distribution",
                                        labels={"MonthlyIncome": "Monthly Income", "count": "Frequency"},
                                        template="plotly")
st.plotly_chart(monthly_income_histogram)


# Add pie chart for attrition distribution among job roles
st.subheader("Attrition Distribution Among Job Roles")
attrition_pie = px.pie(filtered_df, names="JobRole",hole=0.2, title="Attrition Distribution Among Job Roles")
st.plotly_chart(attrition_pie)

# Heatmap to explore correlation between factors
st.subheader("Correlation Heatmap")
correlation_matrix = filtered_df.corr()
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
st.pyplot(heatmap.figure)


# Employee performance based on role 


# Display the raw data
with st.expander("View Raw Data"):
    st.write(filtered_df)
