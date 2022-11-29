/*
Shoex Token Mintable
*/

pragma solidity ^0.5.17;

//  Import the following contracts from the OpenZeppelin library:
//    * `ERC20`
//    * `ERC20Detailed`
//    * `ERC20Mintable`
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

// Create a constructor for the ShoexToken contract and have the contract inherit the imported libraries from OpenZeppelin.

contract ShoexToken is ERC20, ERC20Detailed, ERC20Mintable {
    constructor(
        string memory name,
        string memory symbol,
        uint initial_supply
    )
    ERC20Detailed(name, symbol, 18)
    public
    {
        // constructor can stay empty
    }   
    
}