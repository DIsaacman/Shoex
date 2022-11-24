import streamlit as st
import pandas as pd
import csv

st.write("# Collecting user email address")

user_name = st.text_input("Please enter your name")

user_email = st.text_input("Please enter your email address")

if st.button("Display the user record"):
    st.write(f"User name is {user_name}")
    st.write(f"User email address is {user_email}")

#create a dataframe 
d = {'user_name': [user_name], 'user_email': [user_email]}
df= pd.DataFrame(data=d)

# Display the dataframe to streamlit
st.write(df)

#Export dataframe to designated folder
df.to_csv('..\Resources\useremail.csv')