import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
import time
load_dotenv()

st.set_page_config(
    page_title="Shoex Sales",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Change the background image
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1590859808308-3d2d9c515b1a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2074&q=80");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Load Asset
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_xj8yh6ox.json")
#img_shoex = Image.open("")

# Horizontal menu
selected = option_menu(
    menu_title=None,
    options=["Crowdsale", "White Paper"],
    icons=["house","book"],
    menu_icon="cast",
    default_index = 0,
    orientation="horizontal",
)

if selected == "Crowdsale":
    with st.container():
        st.markdown("<h1 style='text-align: center; color: white;'>Shoex Presale</h1>", unsafe_allow_html=True)


    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        
        with left_column:
            st.write("put text here")

        with right_column:
            st_lottie(lottie_coding, height=300, key="coding")


if selected == "White Paper":
    st.title(f"You have selected {selected}")


    
# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("project_3/style/style.css")

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
