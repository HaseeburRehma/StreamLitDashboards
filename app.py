import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


st.set_page_config(page_title="Survey Dashboard",  page_icon=":bar_chart:", layout="wide")


#st.set_page_config(page_title='Survey Results')
st.header('Survey Results 2024')
st.subheader('Deparment Survey Annual Report')

### --- LOAD DATAFRAME
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D', 
                   header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='F:G',
                                header=3)
df_participants.dropna(inplace=True)




# --- STREAMLIT SELECTION
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))

department_selection = st.multiselect('Department:',
                                    department,
                                    default=department)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()



# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   color_discrete_sequence = ['blue']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('surveyimg.png')
col1.image(image,
        caption='Designed by freeppik',
        use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Total No. of Participants',
                values='Participants',
                names='Departments',
                hole= 0.3)

st.plotly_chart(pie_chart)



# --- PLOT BOX PLOT
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df[mask], x='Department', y='Rating', palette='Set3', ax=ax)
ax.set_title('Rating Distribution by Department')
ax.set_xlabel('Department')
ax.set_ylabel('Rating')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)



# Initialize LabelEncoder
#label_encoder = LabelEncoder()

# Encode the 'Department' column
#df['Department_Encoded'] = label_encoder.fit_transform(df['Department'])

# Now, replace the 'Department' column with the encoded values
#department_encoded_selection = label_encoder.transform(department_selection)

# Update mask to use the encoded department values
#mask = (df['Age'].between(*age_selection)) & (df['Department_Encoded'].isin(department_encoded_selection))

# --- PLOT HEATMAP
##fig, ax = plt.subplots(figsize=(10, 8))
#sns.heatmap(df[mask].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
#ax.set_title('Correlation Heatmap')
#st.pyplot(fig)

# --- PLOT SCATTER PLOT
#fig, ax = plt.subplots(figsize=(10, 6))
#sns.scatterplot(data=df[mask], x='Age', y='Rating', hue='Department', palette='Set2', ax=ax)
#ax.set_title('Age vs. Rating')
#ax.set_xlabel('Age')
#ax.set_ylabel('Rating')
#st.pyplot(fig)
 

