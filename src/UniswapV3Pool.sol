// SPDX-License-Identifier: MIT
pragma solidity ^0.8.14;
import {Position} from "./lib/Position.sol";
import {Tick} from "./lib/Tick.sol";


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
}