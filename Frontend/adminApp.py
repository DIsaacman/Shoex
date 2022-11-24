import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# from crypto_wallet import generate_account, get_balance, send_transaction
from investor_wallet import generate_account, get_balance

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contracts ABI
    with open(Path('../Backend/contracts/compiled/ShoexTokenPreCrowdsale_abi.json')) as f:
        artwork_presale_abi = json.load(f)
    with open(Path('../Backend/contracts/compiled/ShoexTokenCrowdsale_abi.json')) as f1:
        artwork_crowdsale_abi = json.load(f1)
   

    # Set the presale contract address (this is the address of the deployed contract)
    presale_contract_address = os.getenv("PRE_SALE_SMART_CONTRACT_ADDRESS")

    # Get the presale contract
    presale_contract = w3.eth.contract(
        address=presale_contract_address,
        abi=artwork_presale_abi
    )
    
    # Set the crowdsale contract address (this is the address of the deployed contract)
    crowdsale_contract_address = os.getenv("SALE_SMART_CONTRACT_ADDRESS")

    # Get the crowdsale contract
    crowdsale_contract = w3.eth.contract(
        address=crowdsale_contract_address,
        abi=artwork_crowdsale_abi
    )

    return presale_contract, crowdsale_contract


# Load the contract
presale_contract, crowdsale_contract = load_contract()


################################################################################
# Register Shoex Crowdsale
################################################################################
token_price = 0
def get_crowdsaledetails():
    st.sidebar.markdown("## Shoex crowdsale details")
    
    pre_isOpen = presale_contract.functions.isOpen().call()
    ico_isOpen = crowdsale_contract.functions.isOpen().call()

    stage = "Starting soon"
    weiraised = 0
    
    if(pre_isOpen):
        stage = "Presale"
        token_price = presale_contract.functions.rate().call()
        presale_weiraised = presale_contract.functions.weiRaised().call()
        weiraised = presale_weiraised
        # status = "Open"
    elif(ico_isOpen):    
        stage = "Public ICO"
        token_price = crowdsale_contract.functions.rate().call()
        ico_weiraised = crowdsale_contract.functions.weiRaised().call()
        weiRaised = ico_weiraised
        # status = crowdsale_contract.functions.isOpen().call()
        finalised = "No"    
        if crowdsale_contract.functions.finalized().call():
            finalised = "Yes"
    else:
        stage = "Closed"
        token_price = crowdsale_contract.functions.rate().call()
        # weiraised = presale_weiraised + ico_weiraised
        # status = "Close"

    # Display Data
    st.sidebar.write("#### Active Stage ",stage)    
    st.sidebar.write("#### Rate ",token_price)
    st.sidebar.write("#### Wei Raised ",weiraised)    
    if(stage == "Public ICO"):
        st.sidebar.write("#### Goal ",crowdsale_contract.functions.goal().call())
  
    # st.sidebar.write("#### Status ",status)
    st.sidebar.write("#### Opening Time ",crowdsale_contract.functions.openingTime().call())
    st.sidebar.write("#### Closing Time ",crowdsale_contract.functions.closingTime().call())
   
st.title("Shoex Crowdsale")

get_crowdsaledetails()

# token_price = crowdsale_contract.functions.rate().call()

#----------------------------------------------------------------------------------------------------------------------
# Transaction functionality designs
#----------------------------------------------------------------------------------------------------------------------
from web3.gas_strategies.time_based import medium_gas_price_strategy
def buy_token(w3, beneficiary, total_price):
    # Set gas price strategy
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    # Convert eth amount to Wei
    value = w3.toWei(total_price, "ether")
    st.write(value)

    # Calculate gas estimate
    gasEstimate = w3.eth.estimateGas(
        {"from": beneficiary.address, "value": value})
    # Construct a raw transaction
    txn={
        'from': beneficiary.address,
        'value': value, 
        'gas': gasEstimate,
        'gasPrice': 0,
        'nonce': w3.eth.get_transaction_count(beneficiary.address)
        }

    

    # Sign the raw transaction with ethereum account
    signed_txn=beneficiary.signTransaction(txn)

    crowdsale_contract.functions.buyTokens(beneficiary.address).buildTransaction(txn)

    # Send the signed transactions
    return w3.eth.sendRawTransaction(signed_txn.rawTransaction)


accounts = w3.eth.accounts
address = st.selectbox("Ganache Accounts", options=accounts)
investor_account = generate_account()
number_of_tokens = st.number_input("Number of Tokens Purchasing", step = 1)


# Click button to buy tokens
if st.button("Buy Token"):
    
    # Write total cost of tokens
    st.markdown("## Total Token Cost in Ether")
    st.markdown(token_price)
    st.markdown(number_of_tokens)
    st.markdown(investor_account.address)
    total_cost = token_price * number_of_tokens
    st.write(total_cost)

    transaction_hash = buy_token(w3, investor_account, total_cost)

    # Calculate remaining number of tokens available for sale
    # total_supply = token_contract.functions.totalSupply().call()
    # cap = crowdsale_contract.functions.cap().call()
    # remaining_tokens = cap - total_supply
    # write_supply()

    # Write available token balance
    # st.sidebar.write("#### Only ", remaining_tokens, "amount of tokens are available")

    # Markdown for the transaction hash
    st.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()