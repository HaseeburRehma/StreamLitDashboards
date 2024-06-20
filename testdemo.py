import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import seaborn as sns

# Load data from testDemo.csv and ENCS.xlsx with specified encoding
test_demo_file = 'testDemo1.xlsx'
test_demo_df = pd.read_excel(test_demo_file)

encs_file = 'ENCS.xlsx'
encs_df = pd.read_excel(encs_file, sheet_name='Tasks')

# Convert date columns to datetime format
test_demo_df['Start Date'] = pd.to_datetime(test_demo_df['Start Date'], errors='coerce')
test_demo_df['Due Date'] = pd.to_datetime(test_demo_df['Due Date'], errors='coerce')
encs_df['Start Date'] = pd.to_datetime(encs_df['Start Date'], errors='coerce')
encs_df['Due Date'] = pd.to_datetime(encs_df['Due Date'], errors='coerce')

# Fill missing values
encs_df.fillna('', inplace=True)
test_demo_df.fillna('', inplace=True)

# Convert 'Assigned To' columns to string to handle mixed types and fill NaN with 'Unknown'
test_demo_df['Assigned To'] = test_demo_df['Assigned To'].astype(str).fillna('Unknown')
encs_df['Assigned To'] = encs_df['Assigned To'].astype(str).fillna('Unknown')


# Function to calculate task evaluation based on status
def calculate_task_evaluation(df):
    if df.empty:
        return pd.DataFrame()

    # Group by Assigned To and Progress
    task_evaluation = df.groupby(['Assigned To', 'Progress']).size().unstack(fill_value=0)
    
    # Initialize columns if they are missing
    if 'Not started' not in task_evaluation.columns:
        task_evaluation['Not started'] = 0
    if 'In progress' not in task_evaluation.columns:
        task_evaluation['In progress'] = 0
    if 'Completed' not in task_evaluation.columns:
        task_evaluation['Completed'] = 0
    
    # Calculate tasks left, not started, in progress, late, completed
    task_evaluation['Tasks Left'] = task_evaluation['Not started'] + task_evaluation['In progress']
    task_evaluation['Not Started'] = task_evaluation['Not started']
    task_evaluation['In Progress'] = task_evaluation['In progress']
    task_evaluation['Completed'] = task_evaluation['Completed']
    
    return task_evaluation[['Tasks Left', 'Not Started', 'In Progress', 'Completed']]

# Function to plot task evaluation pie chart for a member
def plot_task_evaluation_pie_chart(task_evaluation, assignee):
    if task_evaluation.empty or assignee not in task_evaluation.index:
        return plt.figure()

    # Extract data for the selected assignee
    assignee_data = task_evaluation.loc[assignee]
    
    fig, ax = plt.subplots()
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    labels = assignee_data.index
    explode = (0.05, 0.05, 0.05, 0.05)  # explode 1st slice

    ax.pie(assignee_data, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode=explode)
    ax.set_title(f'Task Evaluation for {assignee}')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig


# Streamlit app layout starts here
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Logo and title
image = Image.open('encs-logo.png')  # Update the path if needed
st.image(image, width=100)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    margin-top: 25px;
    }
    </style>
    <center><h1 class="title-test">ENCS & testDemo Dashboard</h1></center>"""
st.markdown(html_title, unsafe_allow_html=True)

# Last updated date
box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
st.write(f"Last updated by:  \n {box_date}")

# Define unique assignees for both datasets
unique_assignees_encs = sorted(set(encs_df['Assigned To']))
unique_assignees_testDemo = sorted(set(test_demo_df['Assigned To']))

# Sidebar for ENCS Data tab
with st.sidebar:
    st.header('Filter Options - ENCS Data')
    selected_assignee_encs = st.selectbox('Select Assigned To:', unique_assignees_encs, key='encs_assignee')
    

# Sidebar for testDemo Data tab
with st.sidebar:
    st.header('Filter Options - testDemo Data')
    selected_assignee_testDemo = st.selectbox('Select Assigned To:', unique_assignees_testDemo, key='test_demo_assignee')

# Define tabs for different datasets
tabs = st.tabs(["ENCS Data", "testDemo Data"])


# Content for ENCS Data tab
with tabs[0]:
    st.header("ENCS Data Visualizations")
    
    # Filter data based on selected assignee
    filtered_encs_df = encs_df[encs_df['Assigned To'] == selected_assignee_encs]
    
    # Define columns for visualizations
    col1, col2 = st.columns([1, 1])  
   
    
         # Task Evaluation
     
    
    
   
    with col1:
        
        st.subheader("Bucket Name Distribution")

        if not filtered_encs_df.empty:
            bucket_counts = filtered_encs_df['Bucket Name'].value_counts()
            fig, ax = plt.subplots(figsize=(12, 7))

            # Creating a bar plot with dynamic color mapping
            colors = sns.color_palette("viridis", len(bucket_counts))
            bar_plot = sns.barplot(x=bucket_counts.index, y=bucket_counts.values, palette=colors, ax=ax)

            # Enhancing the plot aesthetics
            ax.set_xlabel('Bucket Name', fontsize=14)
            ax.set_ylabel('Count', fontsize=14)
            ax.set_title('Distribution of Buckets', fontsize=16, fontweight='bold')

            # Rotating x-axis labels for better readability
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

            # Adding data labels with formatting
            for container in ax.containers:
                ax.bar_label(container, fmt='%.0f', padding=5)

            st.pyplot(fig)
        else:
            st.write("No bucket data available for the selected assignee.")

        task_evaluation_encs = calculate_task_evaluation(filtered_encs_df)
        
        if not task_evaluation_encs.empty:
          st.dataframe(task_evaluation_encs)
          
          # Display Task Evaluation as a pie chart
          st.subheader(f"Task Evaluation Pie Chart for {selected_assignee_encs}")
          fig = plot_task_evaluation_pie_chart(task_evaluation_encs, selected_assignee_encs)
          st.pyplot(fig)
        else:
            st.write("No priority data available for the selected assignee.")
        
    
    

    with col2:
        st.subheader("Distribution of Priorities")
       
        if not filtered_encs_df.empty:
         priority_counts = filtered_encs_df['Priority'].value_counts()
    
         # Sort priorities if there is a specific order, else it will be sorted by value_counts
         sorted_priorities = priority_counts.sort_index(ascending=False)
         
         fig, ax = plt.subplots(figsize=(12, 7))

         # Creating a horizontal bar plot with a dynamic color gradient
         colors = sns.color_palette("viridis", len(sorted_priorities))
         bar_plot = sns.barplot(y=sorted_priorities.index, x=sorted_priorities.values, palette=colors, ax=ax)
    
         # Enhancing the plot aesthetics
         ax.set_xlabel('Count', fontsize=14, fontweight='bold')
         ax.set_ylabel('Priority', fontsize=14, fontweight='bold')
         ax.set_title('Distribution of Priorities', fontsize=16, fontweight='bold')

         # Adding data labels with formatting
         for container in ax.containers:
             ax.bar_label(container, fmt='%.0f', padding=5, label_type='edge', fontsize=12)

         # Removing spines for a cleaner look
         sns.despine(left=True, bottom=True)

         # Adding grid for better readability
         ax.xaxis.grid(True, linestyle='--', linewidth=0.7)
         ax.yaxis.grid(False)

         st.pyplot(fig)
        else:
          st.write("No priority data available for the selected assignee.")

        st.subheader("Priority vs. Progress Status")
        if not filtered_encs_df.empty:
            # Aggregating data
            priority_progress_counts = filtered_encs_df.groupby('Priority')['Progress'].value_counts().unstack().fillna(0)

            fig, ax = plt.subplots(figsize=(14, 8))

            # Plotting stacked bar chart with a color palette
            priority_progress_counts.plot(kind='bar', stacked=True, ax=ax, colormap="viridis")

            # Enhancing plot aesthetics
            ax.set_xlabel('Priority', fontsize=14, fontweight='bold')
            ax.set_ylabel('Count', fontsize=14, fontweight='bold')
            ax.set_title('Priority vs. Progress Status', fontsize=16, fontweight='bold')

            # Adding data labels
            for container in ax.containers:
                ax.bar_label(container, fmt='%.0f', label_type='center', fontsize=10)

            # Rotating x-axis labels for better readability
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

            # Adding legend outside the plot
            ax.legend(title='Progress Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

            # Adding grid for better readability
            ax.yaxis.grid(True, linestyle='--', linewidth=0.7)
            ax.xaxis.grid(False)

            # Removing unnecessary spines
            sns.despine(left=True, bottom=True)

            st.pyplot(fig)
        else:
            st.write("No priority vs. progress data available for the selected assignee.")
   

    st.subheader("Task Status by Assignee")
    if not filtered_encs_df.empty:
        fig, ax = plt.subplots(figsize=(16, 10))

        # Grouping data and creating a horizontal stacked bar plot
        task_status_counts = filtered_encs_df.groupby(['Assigned To', 'Progress']).size().unstack(fill_value=0)
        task_status_counts.plot(kind='barh', stacked=True, colormap="plasma", ax=ax)

        # Enhancing plot aesthetics
        ax.set_title('Task Status by Assignee', fontsize=18, fontweight='bold')
        ax.set_xlabel('Number of Tasks', fontsize=14)
        ax.set_ylabel('Assignee', fontsize=14)

        # Adding data labels for each segment
        for container in ax.containers:
            labels = [f'{int(v)}' if v > 0 else '' for v in container.datavalues]
            ax.bar_label(container, labels=labels, label_type='center', fontsize=10, padding=5)

        # Customizing legend and positioning it outside the plot
        ax.legend(title='Progress Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

        # Adding grid for better readability
        ax.xaxis.grid(True, linestyle='--', linewidth=0.7)
        ax.yaxis.grid(False)

        # Rotating x-axis labels
        plt.xticks(rotation=0, ha='center')

        # Removing unnecessary spines for a cleaner look
        sns.despine(left=True, bottom=True)

        st.pyplot(fig)
    else:
        st.write("No data available for the selected assignee.")
    

    st.subheader("Tasks Due Over Time")
    if not filtered_encs_df.empty:
        filtered_encs_df['Due Date'] = pd.to_datetime(filtered_encs_df['Due Date'], errors='coerce')
        due_dates = filtered_encs_df['Due Date'].dropna()
        due_date_counts = due_dates.value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(14, 6))
        due_date_counts.plot(kind='line', marker='o', ax=ax, color='b')
        ax.set_title('Tasks Due Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Tasks Due')
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %d'))
        ax.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=1))
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("No due date data available for the selected assignee.")

# Content for testDemo Data tab
with tabs[1]:
    st.header("testDemo Data Visualizations")
    
    # Filter data based on selected assignee
    filtered_test_demo_df = test_demo_df[test_demo_df['Assigned To'] == selected_assignee_testDemo]
    
    # Define columns for visualizations
    col3, col4 = st.columns([1, 1])  # 2 columns layout for testDemo Data tab
    
    with col3:
        st.subheader("Bucket Name Distribution")
        if not filtered_test_demo_df.empty:
            bucket_counts = filtered_test_demo_df['Bucket Name'].value_counts()
            fig, ax = plt.subplots(figsize=(12, 7))

            # Creating a bar plot with dynamic color mapping
            colors = sns.color_palette("viridis", len(bucket_counts))
            bar_plot = sns.barplot(x=bucket_counts.index, y=bucket_counts.values, palette=colors, ax=ax)

            # Enhancing the plot aesthetics
            ax.set_xlabel('Bucket Name', fontsize=14)
            ax.set_ylabel('Count', fontsize=14)
            ax.set_title('Distribution of Buckets', fontsize=16, fontweight='bold')

            # Rotating x-axis labels for better readability
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

            # Adding data labels with formatting
            for container in ax.containers:
                ax.bar_label(container, fmt='%.0f', padding=5)

            st.pyplot(fig)
        else:
            st.write("No bucket data available for the selected assignee.")

        task_evaluation_encs = calculate_task_evaluation(filtered_test_demo_df)
        
        if not task_evaluation_encs.empty:
          st.dataframe(task_evaluation_encs)
          
          # Display Task Evaluation as a pie chart
          st.subheader(f"Task Evaluation Pie Chart for {selected_assignee_testDemo}")
          fig = plot_task_evaluation_pie_chart(task_evaluation_encs, selected_assignee_testDemo)
          st.pyplot(fig)
        else:
            st.write("No priority data available for the selected assignee.")

    with col4:
        st.subheader("Priority Distribution")
        if not filtered_test_demo_df.empty:
         priority_counts = filtered_test_demo_df['Priority'].value_counts()
    
         # Sort priorities if there is a specific order, else it will be sorted by value_counts
         sorted_priorities = priority_counts.sort_index(ascending=False)
         
         fig, ax = plt.subplots(figsize=(12, 7))

         # Creating a horizontal bar plot with a dynamic color gradient
         colors = sns.color_palette("viridis", len(sorted_priorities))
         bar_plot = sns.barplot(y=sorted_priorities.index, x=sorted_priorities.values, palette=colors, ax=ax)
    
         # Enhancing the plot aesthetics
         ax.set_xlabel('Count', fontsize=14, fontweight='bold')
         ax.set_ylabel('Priority', fontsize=14, fontweight='bold')
         ax.set_title('Distribution of Priorities', fontsize=16, fontweight='bold')

         # Adding data labels with formatting
         for container in ax.containers:
             ax.bar_label(container, fmt='%.0f', padding=5, label_type='edge', fontsize=12)

         # Removing spines for a cleaner look
         sns.despine(left=True, bottom=True)

         # Adding grid for better readability
         ax.xaxis.grid(True, linestyle='--', linewidth=0.7)
         ax.yaxis.grid(False)

         st.pyplot(fig)
        else:
          st.write("No priority data available for the selected assignee.")

        st.subheader("Priority vs. Progress Status")
        if not filtered_test_demo_df.empty:
            # Aggregating data
            priority_progress_counts = filtered_test_demo_df.groupby('Priority')['Progress'].value_counts().unstack().fillna(0)

            fig, ax = plt.subplots(figsize=(14, 8))

            # Plotting stacked bar chart with a color palette
            priority_progress_counts.plot(kind='bar', stacked=True, ax=ax, colormap="viridis")

            # Enhancing plot aesthetics
            ax.set_xlabel('Priority', fontsize=14, fontweight='bold')
            ax.set_ylabel('Count', fontsize=14, fontweight='bold')
            ax.set_title('Priority vs. Progress Status', fontsize=16, fontweight='bold')

            # Adding data labels
            for container in ax.containers:
                ax.bar_label(container, fmt='%.0f', label_type='center', fontsize=10)

            # Rotating x-axis labels for better readability
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

            # Adding legend outside the plot
            ax.legend(title='Progress Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

            # Adding grid for better readability
            ax.yaxis.grid(True, linestyle='--', linewidth=0.7)
            ax.xaxis.grid(False)

            # Removing unnecessary spines
            sns.despine(left=True, bottom=True)

            st.pyplot(fig)
        else:
            st.write("No priority vs. progress data available for the selected assignee.")
        

    st.subheader("Task Status by Assignee")
    if not filtered_test_demo_df.empty:
        fig, ax = plt.subplots(figsize=(16, 10))

        # Grouping data and creating a horizontal stacked bar plot
        task_status_counts = filtered_test_demo_df.groupby(['Assigned To', 'Progress']).size().unstack(fill_value=0)
        task_status_counts.plot(kind='barh', stacked=True, colormap="plasma", ax=ax)

        # Enhancing plot aesthetics
        ax.set_title('Task Status by Assignee', fontsize=18, fontweight='bold')
        ax.set_xlabel('Number of Tasks', fontsize=14)
        ax.set_ylabel('Assignee', fontsize=14)

        # Adding data labels for each segment
        for container in ax.containers:
            labels = [f'{int(v)}' if v > 0 else '' for v in container.datavalues]
            ax.bar_label(container, labels=labels, label_type='center', fontsize=10, padding=5)

        # Customizing legend and positioning it outside the plot
        ax.legend(title='Progress Status', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

        # Adding grid for better readability
        ax.xaxis.grid(True, linestyle='--', linewidth=0.7)
        ax.yaxis.grid(False)

        # Rotating x-axis labels
        plt.xticks(rotation=0, ha='center')

        # Removing unnecessary spines for a cleaner look
        sns.despine(left=True, bottom=True)

        st.pyplot(fig)
    else:
        st.write("No data available for the selected assignee.")
   

    st.subheader("Tasks Due Over Time")
    if not filtered_test_demo_df.empty:
        filtered_test_demo_df['Due Date'] = pd.to_datetime(filtered_test_demo_df['Due Date'], errors='coerce')
        due_dates = filtered_test_demo_df['Due Date'].dropna()
        due_date_counts = due_dates.value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(14, 6))
        due_date_counts.plot(kind='line', marker='o', ax=ax, color='b')
        ax.set_title('Tasks Due Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Tasks Due')
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %d'))
        ax.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=1))
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.write("No due date data available for the selected assignee.")

# Display the app
st.write("### Overview of Tasks and Progress")
st.write("Explore different visualizations based on filters selected in the sidebar.")
