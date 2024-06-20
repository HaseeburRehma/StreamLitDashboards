import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from office365_api import SharePoint  # Assuming this is your office365_api.py with SharePoint class

# Streamlit UI setup
st.header("SharePoint Data Visualizations")

# Initialize SharePoint instance
sharepoint = SharePoint()

# Load data from SharePoint
try:
    # Example: Downloading the latest file from a SharePoint folder
    folder_name = 'Hanif Bahadur'  # Replace with your folder name in SharePoint
    latest_file_name, file_content = sharepoint.download_latest_file(folder_name)
    
    if file_content:
        # Assuming the content is CSV data
        sharepoint_df = pd.read_csv(StringIO(file_content.decode('utf-8')))
        st.write("Data loaded successfully from SharePoint.")
        
        unique_assignees_sharepoint = sorted(set(sharepoint_df['Assigned To']))
        selected_assignee_sharepoint = st.selectbox('Select Assigned To:', unique_assignees_sharepoint, key='sharepoint_assignee')
        filtered_sharepoint_df = sharepoint_df[sharepoint_df['Assigned To'] == selected_assignee_sharepoint]
        
        col1, col2 = st.columns([1, 1])  # 2 columns layout for SharePoint Data tab
        
        with col1:
            st.subheader("Bucket Name Distribution")
            if not filtered_sharepoint_df.empty:
                bucket_counts = filtered_sharepoint_df['Category'].value_counts()
                fig, ax = plt.subplots(figsize=(10, 6))
                bucket_counts.plot(kind='bar', ax=ax)
                ax.set_xlabel('Bucket Name')
                ax.set_ylabel('Count')
                ax.set_title('Bucket Name Distribution')
                st.pyplot(fig)
            else:
                st.write("No bucket data available for the selected assignee.")

            st.subheader("Progress Status Distribution")
            if not filtered_sharepoint_df.empty:
                progress_counts = filtered_sharepoint_df['Progress'].value_counts()
                fig, ax = plt.subplots(figsize=(8, 8))
                progress_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
                ax.set_ylabel('')
                ax.set_title('Progress Status Distribution')
                st.pyplot(fig)
            else:
                st.write("No progress data available for the selected assignee.")

        with col2:
            st.subheader("Priority Distribution")
            if not filtered_sharepoint_df.empty:
                priority_counts = filtered_sharepoint_df['Priority'].value_counts()
                fig, ax = plt.subplots(figsize=(10, 6))
                priority_counts.plot(kind='bar', ax=ax)
                ax.set_xlabel('Priority')
                ax.set_ylabel('Count')
                ax.set_title('Priority Distribution')
                st.pyplot(fig)
            else:
                st.write("No priority data available for the selected assignee.")

            st.subheader("Priority vs. Progress Status")
            if not filtered_sharepoint_df.empty:
                priority_progress_counts = filtered_sharepoint_df.groupby('Priority')['Progress'].value_counts().unstack().fillna(0)
                fig, ax = plt.subplots(figsize=(10, 6))
                priority_progress_counts.plot(kind='bar', stacked=True, ax=ax)
                ax.set_xlabel('Priority')
                ax.set_ylabel('Count')
                ax.set_title('Priority vs. Progress Status')
                st.pyplot(fig)
            else:
                st.write("No priority vs. progress data available for the selected assignee.")

        st.subheader("Task Status by Assignee")
        if not filtered_sharepoint_df.empty:
            fig, ax = plt.subplots(figsize=(14, 8))
            task_status_counts = filtered_sharepoint_df.groupby(['Assigned To', 'Progress']).size().unstack(fill_value=0)
            task_status_counts.plot(kind='barh', stacked=True, ax=ax)
            ax.set_title('Task Status by Assignee')
            ax.set_xlabel('Assignee')
            ax.set_ylabel('Number of Tasks')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.write("No data available for the selected assignee.")
    else:
        st.warning("No data downloaded from SharePoint.")
except Exception as e:
    st.error(f"Error loading data from SharePoint: {e}")
