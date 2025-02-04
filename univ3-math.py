import math

#price range calculation
def price_to_tick(p):
    return math.floor(math.log(p, 1.0001))

#uniswap v3 uses Q64.96 number to store sqrt P, this is a fixed point number that has 64 buts for the integer part and 96 bits for the fractional part
q96 = 2 **96

def price_to_sqrtP(p):
    return int(math.sqrt(p) * q96)


# price ranges can be depleted - it's possible to buy the entire amount of one token from a price range and leave the pool with only the other token
# at the points a and b, there's only one token in the range: ETH and the point a and USDC at the point b
# we want to find an L that will allow the price to move to either of the points
# we want enough liquidity for the price to reach either of the boundaries of a price range, thus we want L to be calculated based on the max amounts of change x and change y

#prices at the edge:
# when ETH is bought from a pool, the price is growing; when usdc is bought, the price is falling
# recall that y/x is price
# so at point a, the price is the lowest of the range; at point b, the price is the highest

# NEW LIQUIDITY MUST NOT CHANGE THE CURRENT PRICE:
# that is, it must be proportional to the current proportion of the reserves and this is why the two L's can be different - when the proportion is not preserved
# and we pick the small L to reestablish the proportion

sqrtp_low = price_to_sqrtP(4545)
sqrtp_curr = price_to_sqrtP(5000)
sqrtp_upp = price_to_sqrtP(5500)

def liquidity0(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    
    numerator = amount * (pa * pb) / q96
    
    denominator = pb - pa 

    return numerator/denominator

def liquidity1(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    
    numerator = amount * q96

    denominator = pb - pa

    return numerator/denominator

eth = 10 ** 18
amount_eth = 1 * eth
amount_usdc = 5000 * eth

liq0 = liquidity0(amount_eth, sqrtp_curr, sqrtp_upp)
liq1 = liquidity1(amount_usdc, sqrtp_curr, sqrtp_low)
liq = int(min(liq0, liq1))

print(liq)

# token amounts calcultion again
# since we choose the amounts we're going to deposit, the amounts can be wrong
# we cannot deposit at any price range; the liquidity amount needs to be distributed evenly along the curve of the price range we're depositing into
# Thus we even though users choose amounts, needs to re-calculate them, and actual amounts will be slightly differenrt

def calc_amount0(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa

    return int(liq * q96 * (pb - pa)/(pa * pb))

def calc_amount1(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    
    return int(liq * (pb - pa)/q96)

amount0 = calc_amount0(liq, sqrtp_upp, sqrtp_curr)
amount1 = calc_amount1(liq, sqrtp_low, sqrtp_curr)
print(amount0, amount1)

#calculate the target swap price
# remember: in V3 we choose the price we want our trade to lead to i.e. swapping changes the current price - moves the price along the curve
# formula: L = change y / change sqrt P
# so change sqrt P = change y / L

# Lets calculate the target price for a usdc swap of 42 tokens i.e. 42 dollars to ether

amount_in = 42 * eth
price_diff = (amount_in * q96) // liq
price_next = sqrtp_curr + price_diff
print("New price:", (price_next / q96) ** 2)
print("New sqrtP:", price_next)
print("New tick:", price_to_tick((price_next / q96) ** 2))

#after finding the target price we can calculate token amounts using the amounts calculation functions
# x = L(sqrt(Pb) - sqrt(Pa)) / (sqrt(Pb)*sqrt(Pa))
# y = L(sqrt(Pb) - sqrt(Pa))

amount_in = calc_amount1(liq, price_next, sqrtp_curr)
amount_out = calc_amount0(liq, price_next, sqrtp_curr)

print("USDC in:", amount_in / eth)
print("ETH out:", amount_out / eth)


# output amount calculation when selling eth (that is: selling token x)
# need to find the target price when selling token x (ETH in our case) and buying token y (USDC in this case)
# change x = change (1/sqrt P) * L
# from this we can find the target price
# sqrt(P target) = (sqrt(P) * L) / (change x * sqrt(P) + L)
# knowing target price, we can find the output amount 

# swap eth for usdc
amount_in = 0.01337 * eth
print(f"\nSelling {amount_in/eth} ETH")

price_next = int((liq * q96 * sqrtp_curr) // (liq * q96 + amount_in * sqrtp_curr))
print("New price:", (price_next / q96) ** 2)
print("New sqrtP:", price_next)
print("New tick:", price_to_tick((price_next / q96) ** 2))

amount_in = calc_amount0(liq, price_next, sqrtp_curr)
amount_out = calc_amount1(liq, price_next, sqrtp_curr)

print("ETH in:", amount_in / eth)
print("USDC out:", amount_out / eth)