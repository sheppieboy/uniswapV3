// SPDX-License-Identifier: MIT
pragma solidity ^0.8.14;
import {Position} from "./lib/Position.sol";
import {Tick} from "./lib/Tick.sol";

error InvalidTickRange();
error ZeroLiquidity();

contract UniswapV3Pool {
    using Tick for mapping(int24 => Tick.Info);
    using Position for mapping (bytes32 => Position.Info);
    using Position for Position.Info;

    int24 internal constant MIN_TICK = -887272;
    int24 internal constant MAX_TICK = -MIN_TICK;

    //pool tokens, immutable
    address public immutable token0;
    address public immutable token1;

    //packing vars that are read together

    struct Slot0 {
        //current sqrt(P)
        uint160 sqrtPriceX96;
        //current tick
        int24 tick;
    }

    Slot0 public slot0;

    //amount of liquidity, L
    uint256 public liquidity;

    //Ticks info
    mapping(int24 => Tick.Info) public ticks;
    mapping(bytes32 => Position.Info) public positions;

    constructor(address _token0, address _token1, uint160 sqrtPriceX96, int24 tick) {
        token0 = _token0;
        token1 = _token1;

        slot0 = Slot0({sqrtPriceX96: sqrtPriceX96, tick: tick});
    }

    //take owners address, to track the owner of liquidity
    //upper and lower ticks, to set the bounds of a price range
    //the amount of liquidity we want to provide
    function mint(address owner, int24 lowerTick, int24 upperTick, uint128 amount) external returns (uint256 amount0, uint256 amount1) {
        
        /* outline of how minting works:
        1. a user specifies a price range and an amount of liquidity
        2. the contract updates the ticks and positions mappings
        3. the contract calculates token amounts the user must send
        4. the contract takes tokens from the user and verifies that the correct amounts were set
        */

        if (lowerTick >= upperTick || lowerTick < MIN_TICK || upperTick > MAX_TICK) revert InvalidTickRange();

        if (amount == 0) revert ZeroLiquidity();

        ticks.update(lowerTick, amount);
        ticks.update(upperTick, amount); 
        Position.Info storage position = positions.get(owner, lowerTick, upperTick);
        position.update(amount);

        //HARDCODED FOR NOW
        amount0 = 0.998976618347425280 ether;
        amount1 = 5000 ether;

        liquidity += uint256(amount);

        uint256 balance0Before;
        uint256 balance1Before;

        if (amount0 > 0) balance0Before = balance0();
        if (amount1 > 0) balance1Before = balance1();

        IUniswapV3MintCallback(msg.sender).uniswapV3MintCallback(amount0, amount1);

        if (amount0 > 0 && balance0Before + amount0 > balance0()) revert InsufficientInputAmount();
        if (amount1 > 0 && balance1Before + amount1 > balance1()) revert InsufficientInputAmount();

    }

    function balance0() internal returns (uint256 balance) {
        balance = IERC20(token0).balanceOf(address(this));
    }

    function balance1() internal returns (uint256 balance) {
        balance = IERC20(token1).balanceOf(address(this));
    }

}
