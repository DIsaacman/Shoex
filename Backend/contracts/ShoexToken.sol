/*
Shoex Token Mintable
*/

pragma solidity ^0.5.17;
// As we aim to create a ERC20 token that is 
//  Import the following contracts from the OpenZeppelin library:
//    * `ERC20`
//    * `ERC20Detailed`
//    * `ERC20Mintable`
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

contract ShoexToken is ERC20, ERC20Detailed ,ERC20Mintable {
    
    address payable owner;
    modifier onlyOwner {
        require(msg.sender == owner, "You do not have permission to mint these tokens!");
        _;
    }

    // constructor to initialise variables when contract is deployed
    // set the Name of the token
    // set the Symbol of the token   
    // set initial supply
    constructor(
        string memory name,
        string memory symbol  
        // uint initial_supply
    )
        ERC20Detailed(name, symbol, 18)
        public
    { 
        owner = msg.sender;           
        //_mint(msg.sender, initial_supply);
     }

    // function mint(address recipient, uint amount) public onlyOwner {
    //     _mint(recipient, amount);
    // }
}
