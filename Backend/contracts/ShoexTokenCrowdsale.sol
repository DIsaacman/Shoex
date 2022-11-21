/*
ShoexTokenCrowdsale
ShoeexToken would be made available to the investers via ShoexTokenCrowdsale
Features of Crowdsale
1. Tokens are minted during purchase.
2. The crowd sale is capped, also there is a minimum and maximum cap set for a buyer as well
3. There will be two rounds of crowdsale -
    Round 1 (PreSale) - this will be a timed sale where Whitelisted investers can buy token at discounted rate,
    Round 2 (PublicSale) - this will be open to all at revisied rate.   
4. Only whitelisted beneficiaries are allowed to buy token during preSale 
5. It's a timed refundable crowdsale this gives investors an option to claim refund incase goal is not met.
6. During preSale funds are transferred to the owners wallet and are non refundable, while during public sale funds are transffered in escrow wallet.    
*/

// @TODO: Add the pragma statement
pragma solidity ^0.5.17;

// import statement for the token contract `ShoexToken.sol` file
import "./ShoexToken.sol";

import "./ShoexTokenPresaleCrowdsale.sol";

// import statement for the OpenZeppelin `Crowdsale` contract.
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/WhitelistCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundableCrowdsale.sol";


contract ShoexTokenCrowdsale is Crowdsale, MintedCrowdsale, CappedCrowdsale, TimedCrowdsale, WhitelistCrowdsale,RefundableCrowdsale {
    
    address payable owner;
    modifier onlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _;
    }

    // Set investor cap and track investor contributions
    uint256 public investorMinCap = 2000000000000000;// .002 ether   

    //TODO: Consider to be calculated based on _cap no investor can buy more than 5% of cap  
	uint256 public investorHardCap = 50000000000000000000; // 50 ether
    mapping(address => uint256) public contributions;

    //Define an enum CrowdsaleStage for crowdsale stages       
    enum CrowdsaleStage {PreSale,PublicSale}       
    //Declare public CrowdsaleStage variable to track current Stage, the variable default to presale stage      
    CrowdsaleStage public Stage = CrowdsaleStage.PublicSale;
    PresaleCrowdsale _preSale;
        
    constructor(
        uint256 _rate,
        address payable _wallet,
        ShoexToken _token,
        uint256 _cap,
        uint256 _openingTime,
        uint256 _closingTime,
        uint256 _goal        
    )
      Crowdsale(_rate, _wallet, _token)                 
      CappedCrowdsale(_cap)
      TimedCrowdsale(_openingTime,_closingTime)
      RefundableCrowdsale(_goal) 
                     
      public
    {   
        require(_cap <= _goal) ;

        //TODO: Discuss with team
        require((_cap * 5) >= 10_000);
        investorHardCap = _cap * 5 / 10_000;
        
    }
    
    /**
     * @dev Extend parent behavior requiring purchase to respect the investor funding cap, and allow only whitelisted beneficary during Presale.
     * @param _beneficiary Token purchaser
     * @param _weiAmount Amount of wei contributed
     */
    function _preValidatePurchase(
        address _beneficiary,uint256 _weiAmount
        )
        internal view 
    {   
        //super._preValidatePurchase(_beneficiary,_weiAmount);  

        //Check if stage is preSale only whitelisted beneficiary can buy tokens 
        if(Stage == CrowdsaleStage.PreSale) 
        {
            require(isWhitelisted(_beneficiary), "ShoexTokenCrowdsale: beneficiary doesn't have the Whitelisted role"); 
        }        
        uint256 existingContribution = contributions[_beneficiary];
        uint256 newContribution = existingContribution.add(_weiAmount);
        require(newContribution >= investorMinCap && newContribution <= investorHardCap,"CappedCrowdsale: total invester contribution not with invester cap");
        
        contributions[_beneficiary].add(newContribution);        

    }
      
    /**
     * @dev allows owner to setCrowdsaleStage
     * @param _stage uint that represents Stage     
     */  
    function setCrowdsaleStage(uint _stage) public onlyOwner { 
        if(uint(CrowdsaleStage.PreSale) == _stage)
        {
            Stage = CrowdsaleStage.PreSale;            
        } else if(uint(CrowdsaleStage.PublicSale) == _stage)
        {
            Stage = CrowdsaleStage.PublicSale;
        }       

    }
    /**
     * @dev Overrides Crowdsale fund forwarding, forward funds to wallet during preSale then in escro wallet during public sale
     */
    function _forwardFunds() internal {        
        if(Stage == CrowdsaleStage.PreSale) 
        {
            wallet().transfer(msg.value);

        } else if(CrowdsaleStage.PublicSale == Stage)
        {
            super._forwardFunds();
        }  
    }

    function setupPresale(uint256 rate,uint256 openingTime, uint256 closingTime) public onlyOwner
    {
        //TODO: set pre-sale rate and duration, discuss with team 
    }

    // function setupRate(uint256 rate) public onlyOwner
    // {
         //TODO : Discuss before moving forward
    // }

}


contract ShoexTokenCrowdsaleDeployer {

    // Add public addresses to keep track of the shoex_token_address and shoex_crowdsale_address
    address public shoex_token_address;
    address public shoex_crowdsale_address;

    constructor(
        string memory _name,
        string memory _symbol,
        uint _rate,
        //uint256 _initial_supply,
        address payable _wallet, // this address will receive all Ether raised by the sale
        uint256 _cap,
        uint256 _openingTime,
        uint256 _closingTime,
        uint256 _goal 
    )        
        public
    {
        // create the ShoexToken and its address
        //ShoexToken shxtoken = new ShoexToken(_name,_symbol,_initial_supply);
        ShoexToken shxtoken = new ShoexToken(_name,_symbol);
        shoex_token_address = address(shxtoken);        

        //TODO: just added for testing to remove after integration with fromtend        
        _openingTime = now;
        _closingTime = now + 5 minutes;

        // create the ShoexTokenCrowdsale and its address
        ShoexTokenCrowdsale shxCrowdSale = new ShoexTokenCrowdsale(_rate,_wallet,shxtoken,_cap,_openingTime,_closingTime,_goal);
        shoex_crowdsale_address = address(shxCrowdSale);

        // make the ShoexTokenCrowdsale contract a minter, then have the ShoexTokenCrowdsaleDeployer renounce its minter role
        shxtoken.addMinter(shoex_crowdsale_address);
        shxtoken.renounceMinter();
    }
}
