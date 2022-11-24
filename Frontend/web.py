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
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
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
    options=["Home", "Projects", "Contact"],
    icons=["house","book","envelope"],
    menu_icon="cast",
    default_index = 0,
    orientation="horizontal",
)

if selected == "Home":
    with st.container():
        st.markdown("<h1 style='text-align: center; color: white;'>Shoex Presale</h1>", unsafe_allow_html=True)
        st.title("Get early access to ShoeX Presale. Buy the Sneaky coin now. :tada:")
        st.write("The Sneaky coin will act as a digital token that provides individuals and organizations the ability to exchange value backed by physical rare sneaker collections. The tokens will operate as part of a secure blockchain ledger that tracks and audits the collection.")
        st.write("[White Paper > ] (https://www.youtube.com/watch?v=VqgUkExPvLY)")

    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        
        with left_column:
            st.markdown("<h1 style='text-align: center; color: white;'>How to buy</h1>", unsafe_allow_html=True)
            st.subheader("Step One - Install Wallet")
            st.write("First, make sure you have the MetaMask wallet installed on your browser, or if you’re on mobile use Wallet Connect to connect one of the supported wallets (we recommend Trust Wallet). Purchasing from a desktop browser will give you a smoother buying experience. For this we recommend Metamask. If you are buying on a mobile phone, we recommend using Trust Wallet and connecting through the built-in browser.")
            st.subheader("Step Two - Connect Wallet")
            st.write("Once you have your preferred wallet provider ready, click “Connect Wallet” and select the appropriate option. For mobile wallet apps you will need to select “Wallet Connect” and select “Trust Wallet”. Then you will have 3 options to choose from.")
            st.subheader("Step Three - Claim Token")
            st.write("After the pre-sale is over, you will be able to claim your D2T tokens. We'll post the details closer, but you'll need to visit the main site https://dash2trade.com/presale and click the 'Claim' button.")

        with right_column:
            st_lottie(lottie_coding, height=300, key="coding")

    with st.container():
        st.write("---")
        st.markdown("<h1 style='text-align: center; color: white;'>What is Shoex</h1>", unsafe_allow_html=True)

    with st.container():
        st.write("---")
        st.markdown("<h1 style='text-align: center; color: white;'>Road Map</h1>", unsafe_allow_html=True)

    with st.container():
        st.write("---")
        st.markdown("<h1 style='text-align: center; color: white;'>Tokenomics Explained</h1>", unsafe_allow_html=True)

    with st.container():
        st.write("---")
        st.markdown("<h1 style='text-align: center; color: white;'>Meet the team</h1>", unsafe_allow_html=True)    

if selected == "Projects":
    st.title(f"You have selected {selected}")

if selected == "Contact":
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

# Timer
def count_down(ts):
    #with st.empty():
    while ts:
        mins, secs = divmod(ts,60)
        time_now = '{:02d}:{:02d}'.format(mins,secs)
        st.header(time_now)
        time.sleep(1)
        ts -= 1
    st.header("Time up!!")

count_down(10)

