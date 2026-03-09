import numpy as np
from scipy.stats import norm

def black_scholes (S, K, r, T, sigma, option_type='call'):
    option_type = option_type.lower()
    d1 = (np.log(S/K) + (r+ sigma**2/2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call' :
        price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    else :
        price = K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price

