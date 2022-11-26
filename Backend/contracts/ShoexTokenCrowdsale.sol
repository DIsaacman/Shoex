pragma solidity ^0.5.17;

import "./ShoexToken.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundablePostDeliveryCrowdsale.sol";

// Have the ShoexTokenCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
// * CappedCrowdsale
// * TimedCrowdsale
// * RefundablePostDeliveryCrowdsale

contract ShoexTokenCrowdsale is Crowdsale, MintedCrowdsale, CappedCrowdsale, TimedCrowdsale, RefundablePostDeliveryCrowdsale { // UPDATE THE CONTRACT SIGNATURE TO ADD INHERITANCE
    
    mapping(address => uint256) public contributions; // mapping for beneficiary and it's total contribution

    uint256 investorHardCap = 0;    

    address[] _whitelisteds;
    
     

    // Provide parameters for all of the features of your crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(
        uint256 rate, // rate in TKNbits
        address payable wallet, // sale beneficiary
        ShoexToken token, // the ShoexToken itself that the ShoexToken Crowdsale will work with
        uint256 investorcap, // the cap for each investor
        uint goal, // the crowdsale goal
        uint open, // the crowdsale opening time
        uint close // the crowdsale closing time
    ) public
        Crowdsale(rate, wallet, token)
        CappedCrowdsale(goal) // for successful crowdsale, crowdsale cap is the sale goal. If cap is less then goal crowdsale will always fail.
        TimedCrowdsale(open, close)
        RefundableCrowdsale(goal)
    {
        investorHardCap = investorcap;
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
        super._preValidatePurchase(_beneficiary,_weiAmount);          

        uint256 existingContribution = contributions[_beneficiary];
        uint256 newContribution = existingContribution.add(_weiAmount);
        require( newContribution <= investorHardCap,"CappedCrowdsale: total invester contribution not with invester cap");
        contributions[_beneficiary].add(_weiAmount);            
        
    }

}


contract ShoexTokenCrowdsaleDeployer {
    // Create an `address public` variable called `shoex_token_address`.
    address public shoex_token_address;

    // Create an `address public` variable called `shoex_crowdsale_address`.
    address public shoex_crowdsale_address;

    // Add the constructor.
    constructor(
       uint256 rate,
       string memory name,
       string memory symbol,
       address payable wallet,
       uint256 investorcap,
       uint256 goal
    )
    public 
    {
        // Create a new instance of the ShoexToken contract.
        ShoexToken token = new ShoexToken(name, symbol, 0);
        
        // Assign the token contract’s address to the `shoex_token_address` variable.
        shoex_token_address = address(token);

        // Create a new instance of the `ShoexTokenCrowdsale` contract
        //ShoexTokenCrowdsale shoex_crowdsale = new ShoexTokenCrowdsale(rate, wallet, token, investorcap, goal, now, now + 24 weeks);                           

        ShoexTokenCrowdsale shoex_crowdsale = new ShoexTokenCrowdsale(rate, wallet, token, investorcap, goal, block.timestamp + 15 minutes, block.timestamp + 36 weeks);
        // Assign the `ShoexTokenCrowdsale` contract’s address to the `shoex_crowdsale_address` variable.
        shoex_crowdsale_address = address(shoex_crowdsale);

        // Set the `ShoexTokenCrowdsale` contract as a minter
        token.addMinter(shoex_crowdsale_address);
        
        // Have the `ShoexTokenCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}