import pandas as pd
import numpy as np
import streamlit as st
# Load data from CSV
data = pd.read_csv('Updated_data.csv')

# Clean 'prep_time' column
#data['prep_time'] = data['prep_time'].str.replace('M', '').str.replace('Total in', '').astype(float)
#data['prep_time'].fillna(data['prep_time'].mode()[0], inplace=True)
data=data.dropna()
#print(data.info())

data['ingredients']=data['ingredients'].str.strip().str.replace('\t','').str.replace('\n','')

data['course']=data['course'].replace(['World Breakfast','South Indian Breakfast','North Indian Breakfast','Indian Breakfast'],'Breakfast')
data['course']=data['course'].replace(['One Pot Dish','Brunch','Snack'],'Quick Bites')
data['course']=data['course'].replace(['Lunch','Dinner','Main Course'],'Meal')
data['course']=data['course'].replace(['Side Dish','Appetizer'],'Pre-meal')

data['ingredients']=data['ingredients'].str.lower()
#print(data.shape)
# Streamlit app
st.title('Flavour Fusion')
st.header('Cuisines Recommendation')

option = st.selectbox(
    'Select course:',
    data['course'].unique())

option1 = st.selectbox(
    'Select diet:',
    data['diet'].unique())

filtered_names=[]
title = st.text_input('Ingredients you have'," ")
l=(title.lower().split(' '))
# Filter data
filtered_data = data[(data['course'] == option) & (data['diet'] == option1)]
    # Check if the word is in the text (case-insensitive)
for index, row in filtered_data.iterrows():
         # Assuming row['ingredients'] sometimes contains a float value
    # Now, check if all words in the list `l` are present in the ingredients
    if all(word in row['ingredients'] for word in l):
        # Your code here
        filtered_names.append(row['name'])

# Selectbox for filtered names
selected_name = st.selectbox('Select a name:', filtered_names)
if selected_name:
    # Filter filtered_data based on selected_name
    selected_row = filtered_data[filtered_data['name'] == selected_name]
    
    # Display ingredients of the selected row
    agree = st.checkbox('Instructions')
    ingredient=st.checkbox('Ingredients')
    if agree:
       st.write(selected_row['instructions'].iloc[0])
    if ingredient:
       st.write(selected_row['ingredients'].iloc[0])
    
    selected_image_url = data.loc[data['name'] == selected_name, 'image_url'].iloc[0]
    # Display the image associated with the selected recipe
    st.image(selected_image_url, caption=selected_name, width=400)
