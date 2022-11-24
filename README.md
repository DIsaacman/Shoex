# ShoeX ICO 👟


[![Slides](Images/slides.png)](https://www.canva.com/design/DAFSMNt1blo/9X4HeAGjjSaxhrcrIYRdTQ/view?utm_content=DAFSMNt1blo&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

#### Team Name: The-Great-Pretenders

## Project Overview - Tokenising High-End Sneakers

Shoe flipping is a profitable business. The Sneaky coin will act as a digital token that allows individuals and organisations to exchange value backed by rare physical sneaker collections. 

The tokens will operate as part of a secure blockchain ledger that tracks and audits the sneaker stock. The token will be backed by the sneakers and pegged loosely to the collection's value. This electronic tokenisation will allow the fractional ownership of expensive shoe collections on the open market.

## Features

- **Tokenised Sneaker Ownership** ERC-20 Token on Ethereum Blockchain
- **Machine Learning Driven Algorithms** Data driven analysis for decision making using ML
- **Easy to Use Frontend** Interact directly with the blockchain with intuative User Interface

### Introduction - Sneaky Coin

Blockchains and Distributed Ledger Technology have proven to be successful at tokenising real-world assets. 

We can now take previously indivisible assets and fractionalize the network's stake.

Assets such as Real Estate and Gold have been successfully tokenised using blockchain technology . The digitisation of the assets using smart-contracts significantly benefits the users. Moreover, the tokens are divisible into more affordable units with additional utility.

The User can now participate in the high-end sneaker game without spending time, money and effort to find, buy and then secure the physical sneakers.



---



## Detailed Usage - Buying Tokens

ShoeX will conduct a Pre-Sale to raise funds directly on the Ethereum blockchain as a Crowdsale smart contract in Solidity. In addition, ShoeX will sell digital ERC-20 tokens called Sneaky Coins to raise capital to invest in the sneaker collateral.

The benefit of the ERC-20 standard will be that tokens are immutable,  transparent, and tradable in a peer-to-peer fashion. The tokens can be self custodied and stored in a hardware wallet for safe keeping

## User Instructions



### Front End - Buying Tokens 




### Back End - Tokenisation

The ERC-20 was written in solidity, a smart-contract language on ethereum.

```
pragma solidity ^0.5.17;
```

Tools used were:

- [Ganache](https://trufflesuite.com/ganache/)  to access the ETH test-net

- [Remix IDE](https://remix.ethereum.org/) was leveraged to create, compile and deploy the ERC-20 token.

- [Open Zeppelin](https://docs.openzeppelin.com/contracts/4.x/wizard) was used for the token contract templates.

<details>
  <summary>Click to expand:</summary>
  
```solc
$ contract templates /openseppelin/contracts
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundablePostDeliveryCrowdsale.sol";
```
</details>

- [MetaMask](https://metamask.io/) wallet for interacting with test net and signing transactions.


## Roadmap

![](Images/ShoeX%20Roadmap.png)




## Examples



## Analysis

### Data Analysis & Machine Learning

In order to ensure that the sneaker investments are profitable, we used ML and Data analysis to create models and guidlines for buying Sneakers. 

It is apparent that the best shoe sizes for a profitable return are between 9-11 as shown below.

![](Images/Research_size.png)

The Data was sources from StockX which is a collection of 10,000 shoe sales over a 3 year period.

Python version 3.7 and Sci-Kit-Learn (```sklearn```) were the main tools to create a KNN and Logistic regression model to determine if a shoe would meet a criteria of profitability.

The code below created a profitability column based on if the profit of the shoe was at least 100%. The Bollean value was then converted into a binary integer which was used as a target in the Machine Learning model.

The data was trained tested and split before having several models applied. Oversampling the Data resulted in better accuracy scores to predict if the shoe would be profitable.

In the future, the model will be fitted with higher quality data as part of the ongoing improvement of the project.



```
#Set Profit Margin as a multiple
margin = 1

# Find Profitable Sales and Create New Column Called Profitable to act as a target
df['Profitable'] = (df['%']>= margin )

# Change bool value to integer
df['Profitable'] = df['Profitable'].astype(int)
```

---



![](Images/Shoex%20Token%20Shoes%20Sale%20%20(Poster).png)

