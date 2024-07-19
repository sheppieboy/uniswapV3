import math

#price range calculation
def price_to_tick(p):
    r = math.floor(math.log(p, 1.0001))
    print(r)

#uniswap v3 uses Q64.96 number to store sqrt P, this is a fixed point number that has 64 buts for the integer part and 96 bits for the fractional part
q96 = 2 **96

def price_to_sqrtP(p):
    r = int(math.sqrt(p) * q96)
    print(r)

price_to_tick(5000)
price_to_sqrtP(5000)