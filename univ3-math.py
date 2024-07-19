import math

#price range calculation
def price_to_tick(p):
    r = math.floor(math.log(p, 1.0001))
    print(r)

price_to_tick(5000);