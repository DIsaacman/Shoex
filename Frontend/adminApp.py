################################################################################
# The purpose of this file is to create a streamlit app to run the crowdsale.
# The code in this file is divided into following sections

# Section 1 - Necessary imports

# Section 2 -
#   * loads environment variables
#   * initialises session state, menu tabs and variables used in the file
#   * define and connect to Web3 provider  

# Section 3 -
#   * loads the contract once using cache
#   * connects to the contract using the contract address and ABI

# Section 4 -
#   * Call contract functions to get the current active stage and 
#     real time crowdsale data
#   * Write data to the sidebar

# Section 5 - 
#   * 
#   * 
#   * 
#   * 
#   * 
#   * 
#   * 

################################################################################

# Section 1 - Necessary imports
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

################################################################################
# Section 2 -
# 1. Loads environment variables
# 2. Initialises session state, menu tabs and variables used in the file
# 3. Define and connect to Web3 provider  
################################################################################
# Load environment variables
load_dotenv()

# Initialise session state
if "load_state" not in st.session_state:
     st.session_state.load_state = False

# Create streamlit app menu tabs
tab1, tab2, tab3 = st.tabs(["Crowdsale", "Register", "Whitepaper"])

# initialise variables
stage = "Starting soon"
tabHeader = ""
token_price = 0

# Define and connect a Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Section 3 - Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################
@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contracts ABI
    with open(Path('../Backend/contracts/compiled/ShoexTokenPreCrowdsale_abi.json')) as f:
        presale_abi = json.load(f)
    with open(Path('../Backend/contracts/compiled/ShoexTokenCrowdsale_abi.json')) as f1:
        crowdsale_abi = json.load(f1)
   

    # Set the presale contract address (this is the address of the deployed contract)
    presale_contract_address = os.getenv("PRE_SALE_SMART_CONTRACT_ADDRESS")

    # Get the presale contract
    presale_contract = w3.eth.contract(
        address=presale_contract_address,
        abi=presale_abi
    )
    
    # Set the crowdsale contract address (this is the address of the deployed contract)
    crowdsale_contract_address = os.getenv("SALE_SMART_CONTRACT_ADDRESS")

    # Get the crowdsale contract
    crowdsale_contract = w3.eth.contract(
        address=crowdsale_contract_address,
        abi=crowdsale_abi
    )
   
    return presale_contract, crowdsale_contract


# invoke helper function to load the contract
presale_contract, crowdsale_contract = load_contract()


################################################################################
# Section 4 - Contract Helper function :
# 1. Call contract functions to get the current active stage and 
#    real time crowdsale data 
# 2. Write data to the sidebar
################################################################################
def get_crowdsaledetails():
    st.sidebar.markdown("## Shoex crowdsale details")
    
    # Function call to check status of pre-sale
    pre_isOpen = presale_contract.functions.isOpen().call() 
    
    # Function call to check status of Public ICO
    ico_isOpen = crowdsale_contract.functions.isOpen().call()
    
    weiraised = 0
    presale_weiraised = 0

    if(pre_isOpen):
        # If active stage is pre-sale, update stage variable and get presale data by making contract function calls
        stage = "Presale"
        token_price = presale_contract.functions.rate().call()
        presale_weiraised = presale_contract.functions.weiRaised().call()
        weiraised = presale_weiraised        
        tabHeader = "Welcome to Shoex Pre-Crowdsale"
    elif(ico_isOpen):    
        # If active stage is Public ICO, update stage variable and get ICO data by making contract function calls
        stage = "Public ICO"
        token_price = crowdsale_contract.functions.rate().call()
        presale_weiraised = presale_contract.functions.weiRaised().call()
        ico_weiraised = crowdsale_contract.functions.weiRaised().call()
        weiraised = presale_weiraised + ico_weiraised        
        finalised = "No"    
        if crowdsale_contract.functions.finalized().call():
            finalised = "Yes"         
        tabHeader = "Welcome to Shoex Crowdsale"       
    else:
        stage = "Closed"
        token_price = crowdsale_contract.functions.rate().call()
        presale_weiraised = presale_contract.functions.weiRaised().call()
        ico_weiraised = crowdsale_contract.functions.weiRaised().call()
        weiraised = presale_weiraised + ico_weiraised
        # status = "Close"
        # st.title("Shoex Crowdsale is Closed !!")
        tabHeader = "Shoex Crowdsale is Closed !!"          

    # Display Data
    st.sidebar.write("#### Active Stage ",stage)    
    st.sidebar.write("#### Rate ",token_price)
    st.sidebar.write("#### Total ETH Raised ",w3.fromWei(weiraised,'ether'))    
    st.sidebar.write("#### Presale ETH Raised ",w3.fromWei(presale_weiraised,'ether'))    
    if(stage == "Public ICO"):
        st.sidebar.write("#### Goal ",w3.fromWei(crowdsale_contract.functions.goal().call(),'ether'))
  
    # st.sidebar.write("#### Status ",status)
    st.sidebar.write("#### Opening Time ",crowdsale_contract.functions.openingTime().call())
    st.sidebar.write("#### Closing Time ",crowdsale_contract.functions.closingTime().call())
    # crowdsale_contract.functions.buyTokens()

    return stage,tabHeader


st.sidebar.image("../Images/shoex sneaky brand logo (1).png")
# invoke helper function to get real time crowdsale data
stage,tabHeader = get_crowdsaledetails()
 
with tab1:
    st.header(tabHeader)
    #----------------------------------------------------------------------------------------------------------------------
    # Transaction functionality designs
    #----------------------------------------------------------------------------------------------------------------------
    accounts = w3.eth.accounts
    token_price = crowdsale_contract.functions.rate().call()
    if(stage == "Presale"):    
        col1, col2 = st.columns(2)
        whlistedAccounts = []
        genericAccounts = []
        for account in accounts:
            if(presale_contract.functions.isWhitelisted(account).call()):
                whlistedAccounts.append(account)
            else:
                genericAccounts.append(account)                                
        address = st.selectbox("Whitelisted Accounts", options=whlistedAccounts)
        number_of_tokens = st.number_input("Number of Tokens Purchasing", step = 1)    
        
        if st.button("Buy Token"):                          
            total_cost = token_price * number_of_tokens  
            st.markdown("## Total Token Cost in Ether ",total_cost)        
            receipt = None    
            value = w3.toWei(total_cost, "ether")     
            
            transaction_hash = presale_contract.functions.buyTokens(address).transact(
                {"from": address, "value": value, "gas": 2000000})
            st.markdown("#### Validated Transaction Hash")                        
            receipt = w3.eth.waitForTransactionReceipt(transaction_hash)                
            st.write(receipt.transactionHash.hex())
            # Celebrate your successful payment            
            st.balloons()                        
            st.session_state.load_state = True           
            st.experimental_rerun()
        
        genaddress = st.sidebar.selectbox("Generic Accounts", options=genericAccounts)    
        if(st.sidebar.button("Add to Whitelisteds")):
            transaction_hash = presale_contract.functions.addWhitelistedAddress(genaddress).transact({"from": genaddress, "value": 892440000000000,"gas": 2000000})
            receipt = w3.eth.waitForTransactionReceipt(transaction_hash)      
            whlistedAccounts.append(address)
            st.sidebar.write(receipt.transactionHash.hex())
            st.session_state.load_state = True
            st.experimental_rerun()

    elif(stage == "Public ICO"):         
        # Click button to buy tokens
        address = st.selectbox("Ganache Accounts", options=accounts)
        investor_account = address
        number_of_tokens = st.number_input("Number of Tokens Purchasing", step = 1)
        if st.button("Buy Token"):
            
            # Write total cost of tokens
            total_cost = token_price * number_of_tokens    
            st.markdown("## Total Token Cost in Ether ",total_cost)
            
            receipt = None    
            value = w3.toWei(total_cost, "ether")
                        
            transaction_hash = crowdsale_contract.functions.buyTokens(address).transact(
                {"from": address, "value": value, "gas": 2000000})
            receipt = w3.eth.waitForTransactionReceipt(transaction_hash)    
            

            st.markdown("#### Validated Transaction Hash")
            
            st.write(receipt.transactionHash.hex())
            st.session_state.load_state = True            
            # Celebrate your successful payment
            st.balloons()
            st.experimental_rerun()
    st.session_state.load_state = True
with tab2:
    st.header("Stay Connected!!")
    #create dataframe from existing csv
    user_email_df = pd.read_csv(Path("../Resources/useremail.csv"))   
    user_name = st.text_input("Please enter your name")
    user_email = st.text_input("Please enter your email address")
    if st.button("Enter"):
        dicts = {'user_name': user_name, 'user_email':user_email}
        user_email_df = user_email_df.append(dicts,ignore_index=True)
    user_email_df = user_email_df.drop(user_email_df.columns[[0]], axis=1)
    #Export dataframe to designated folder
    user_email_df.to_csv(r'../Resources/useremail.csv')
    st.session_state.load_state = True
with tab3:
    st.write("Click the link to access the Whitepaper")    
    st.markdown("(https://github.com/DIsaacman/Shoex/blob/main/Whitepaper/README.md)")
    st.image("../Images/Whitepaper.png")