import numpy as np
from scipy.stats import norm
from .blackandscholes import black_scholes

def vega(S, K, r, T, sigma):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)


def implied_vol_newton(S, K, r, T, market_price, option_type="call", 
                       sigma_init=0.2, tol=1e-6, max_iter=100):

    sigma = sigma_init

    for _ in range(max_iter):
        price = black_scholes(S, K, r, T, sigma, option_type)
        diff = price - market_price

        if abs(diff) < tol:
            return sigma

        v = vega(S, K, r, T, sigma)
        if v < 1e-8:  # éviter division par zéro
            break

        sigma -= diff / v

    return None  # échec → fallback bisection


def implied_vol_bisection(S, K, r, T, market_price, option_type="call",
                          low=1e-6, high=5.0, tol=1e-6, max_iter=200):

    for _ in range(max_iter):
        mid = 0.5 * (low + high)
        price = black_scholes(S, K, r, T, mid, option_type)

        if abs(price - market_price) < tol:
            return mid

        if price > market_price:
            high = mid
        else:
            low = mid

    return mid


def implied_volatility(S, K, r, T, market_price, option_type="call"):
    """
    Calcule la volatilité implicite en utilisant Newton-Raphson,
    puis fallback bisection si Newton diverge.
    """
    vol = implied_vol_newton(S, K, r, T, market_price, option_type)

    if vol is not None:
        return vol

    return implied_vol_bisection(S, K, r, T, market_price, option_type)