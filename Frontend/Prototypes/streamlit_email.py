import streamlit as st
import pandas as pd
import csv
from pathlib import Path

#create dataframe from existing csv
user_email_df = pd.read_csv(Path("useremail.csv"))

st.write("# Collecting user email address")

user_name = st.text_input("Please enter your name")

user_email = st.text_input("Please enter your email address")

if st.button("Enter"):
    dicts = {'user_name': user_name, 'user_email':user_email}
    user_email_df = user_email_df.append(dicts,ignore_index=True)


user_email_df = user_email_df.drop(user_email_df.columns[[0]], axis=1)
#Export dataframe to designated folder
user_email_df.to_csv(r'C:\Users\micha\OneDrive\Desktop\project3\useremail.csv')
