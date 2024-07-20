// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.14;

import {Test, console} from "forge-std/Test.sol";
import {ERC20Mintable} from "./ERC20Mintable.sol";

contract UniswapV3PoolTest is Test {
    ERC20Mintable token0;
    ERC20Mintable token1;

    function setUp() public {
        token0 = new ERC20Mintable("Ether", "ETH", 18);
        token1 = new ERC20Mintable("USDC", "USDC", 18);
    }

    function testExample() public pure{
        assertTrue(true);
    }
}