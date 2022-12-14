pragma solidity ^0.5.17;

import "./ShoexToken.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";

// Have the ShoexTokenPreCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale - Crowdsale is a base contract for managing a token crowdsale,
//               allowing investors to purchase tokens with ether. This contract implements
//               such functionality in its most fundamental form and can be extended to provide additional
//               functionality and/or custom behavior.
// * MintedCrowdsale - Extension of Crowdsale contract whose tokens are minted in each purchase.
// * TimedCrowdsale  - Crowdsale accepting contributions only within a time frame.
contract ShoexTokenPreCrowdsale is Crowdsale, MintedCrowdsale, TimedCrowdsale {
  
  mapping(address => bool) public whitelisteds; // mapping for beneficiary and it's whitelisted status
  string public Stage = "Presale";
    
  constructor(
    uint256 _rate,
    address payable _wallet,
    ShoexToken _token,
    uint256 _openingTime,
    uint256 _closingTime
  )
    Crowdsale(_rate, _wallet, _token)
    TimedCrowdsale(_openingTime, _closingTime)
        public
  {} 

  /**
     * @dev Extend parent behavior requiring purchase to respect whitelisted beneficary during Presale.
     * @param _beneficiary Token purchaser
     * @param _weiAmount Amount of wei contributed
     */
    function _preValidatePurchase(
        address _beneficiary,uint256 _weiAmount
        )
        internal view 
    {   
        super._preValidatePurchase(_beneficiary,_weiAmount);          
        require( whitelisteds[_beneficiary],"ShoexTokenPreCrowdsale: You are not authorised for pre-sale");                            

    }

    /**
     * @dev public function to add whitelised beneficary
     * @param beneficary Token purchaser     
     */
    function addWhitelistedAddress (address beneficary) public payable
    {
      if(!whitelisteds[beneficary])
      {
        whitelisteds[beneficary] = true;                
                  
      }      
    }

    /**
     * @dev public function to check if a beneficary is whitelised 
     * @param beneficary Token purchaser     
     */
    function isWhitelisted(address beneficary) public view returns (bool) {
      if(whitelisteds[beneficary])
      {
        return true;     
           
      }
        return false;
    }
}

// Contract to deploy ShoexTokenPreCrowdsale contract
contract ShoexTokenPreCrowdsaleDeployer {
    // Create an `address public` variable called `shoex_token_address`.
    address public shoex_token_address;

    // Create an `address public` variable called `shoex_crowdsale_address`.
    address public shoex_pre_crowdsale_address;

    // Add the constructor.
    constructor(
       uint256 rate,
       string memory name,
       string memory symbol,
       address payable wallet       
    )
    public 
    {
        // Create a new instance of the ShoexToken contract.
        ShoexToken token = new ShoexToken(name, symbol, 0);
        
        // Assign the token contract???s address to the `shoex_token_address` variable.
        shoex_token_address = address(token);

        // Create a new instance of the `ShoexTokenPreCrowdsale` contract       

        ShoexTokenPreCrowdsale shoex_pre_crowdsale = new ShoexTokenPreCrowdsale(rate, wallet, token, block.timestamp , block.timestamp + 4 weeks);
        // Assign the `ShoexTokenPreCrowdsale` contract???s address to the `shoex_crowdsale_address` variable.
        shoex_pre_crowdsale_address = address(shoex_pre_crowdsale);

        // Set the `ShoexTokenPreCrowdsale` contract as a minter
        token.addMinter(shoex_pre_crowdsale_address);
        
        // Have the `ShoexTokenPreCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}