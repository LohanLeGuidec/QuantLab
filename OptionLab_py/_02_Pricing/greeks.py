import numpy as np
from scipy.stats import norm

def compute_greeks (S, K, r, T, sigma, option_type='call'): 
    option_type = option_type.lower()
    d1 = (np.log(S/K) + (r + sigma**2/2)) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        delta = norm.cdf(d1)
    else :
        delta = norm.cdf(d1) - 1
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) 
    
    if option_type == 'call':
        theta = -((S * norm.cdf(d1) * sigma) / 2 * np.sqrt(T)) - r * K * np.exp(-r*T) * norm.cdf(d2)
    else : 
        theta = -((S * norm.cdf(d1) * sigma) / 2 * np.sqrt(T)) + r * K * np.exp(-r*T) * norm.cdf(-d2)

    if option_type == 'call':
        rho = K * T * np.exp(-r*T) * norm.cdf(d2)
    else : 
        rho = - K * T * np.exp(-r*T) * norm.cdf(-d2)

    greeks = {
        "Delta" : delta,
        "Gamma" : gamma,
        "Vega" : vega,
        "Theta" : theta,
        "Rho" : rho
    }
    
    return greeks
