import streamlit as st
import pandas as pd
import plotly.express as px
import hydralit_components as hc
import time

st.sidebar.title("ENCS NETWORKS")

# your dashboard content here
df = pd.read_excel("trackerlist.xlsx")

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

col1, col2 = st.columns((2))
df["Start date"] = pd.to_datetime(df["Start date"])

# Getting the min and max date
startDate = pd.to_datetime(df["Start date"]).min()
endDate = pd.to_datetime(df["Due date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start date", startDate))


with col2:
    endDate = pd.to_datetime(st.date_input("Due date", endDate))

#df = df[(df["Start date"] >= date1) & (df["Due date"] <= endDate)].copy()

# Logo
company_logo = "encs-logo.png"

# Display company logo and name in the sidebar
st.sidebar.image(company_logo, use_column_width=True)
st.sidebar.title("ENCS NETWORKS")

# Add some space between the logo and other sidebar content
st.sidebar.markdown("---")
        
        
st.sidebar.header(" Apply your filters: ")

# Create for Assigned to user tasks
assignedto = st.sidebar.multiselect("Pick your Employess", df["Assigned to"].unique())
if not assignedto:
    df2 = df.copy()
else:
    df2 = df[df["Assigned to"].isin(assignedto)]

# Create for task State
taskstate = st.sidebar.multiselect("Pick the Task State", df2["approval"].unique())
if not taskstate:
    df3 = df2.copy()
else:
  df3 = df2[df2["approval"].isin(taskstate)]
  
# Create for Priority
priority = st.sidebar.multiselect("Pick the Task Priority", df["Priority"].unique())
if not priority:
    df4 = df3.copy()
else:
   df4 = df3[df3["Priority"].isin(priority)]
   

# Filter the data based on Assigned to, taskState, and priority
if not assignedto and not taskstate  and not priority:
    filtered_df = df
elif not taskstate  and not priority:
    filtered_df = df[df["Assigned to"].isin(assignedto)]
elif not assignedto  and not priority:
    filtered_df = df[df["approval"].isin(taskstate)]
elif taskstate  and priority:
    filtered_df = df4[df4["approval"].isin(taskstate) & df4["Priority"].isin(priority)]
elif assignedto and priority:
    filtered_df = df4[df4["Assigned to"].isin(assignedto) & df4["Priority"].isin(priority)]
elif assignedto and taskstate:
    filtered_df = df4[df4["Assigned to"].isin(assignedto) & df4["approval"].isin(taskstate)]

else:
   filtered_df = df4[df4["Assigned to"].isin(assignedto) & df4["approval"].isin(taskstate) & df4["priority"].isin(priority)]

#category_df = filtered_df.groupby(by=["approval"], as_index=False)[""].sum()
category_df = filtered_df.groupby("approval")["Assigned to"].count().reset_index()

with col1:
    st.subheader("Category wise Task")
    fig = px.bar(category_df, x="approval", y="Assigned to",
                 text=category_df["Assigned to"],
                 template="plotly",
                 labels={"approval": "Approval Status", "Assigned to": "Count"},
                 color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# Group by "Assigned to" and count the occurrences of each person
assigned_to_df = filtered_df.groupby("Assigned to").size().reset_index(name='Task Count')

with col2:
    st.subheader("Tasks Assigned to Each Person")
    fig = px.pie(assigned_to_df, values='Task Count', names='Assigned to',
                 
                 template="plotly",hole=0.2,
                 color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig, use_container_width=True)


cl1, cl2 = st.columns((2))
priority_df = filtered_df.groupby("Priority").size().reset_index(name='Task Count')

# Plot the bar chart
with cl1:
    st.subheader("Task Priority")
    fig = px.bar(priority_df, x="Priority", y="Task Count",
                 text="Task Count",
                 template="plotly",
                 labels={"Priority": "Priority", "Task Count": "Task Count"},
                 color="Task Count",
                 color_continuous_scale=px.colors.sequential.Blues)
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)