import numpy as np
from .payoffs import european_call, european_put

def simulate_gbm_paths(
    S0, r, sigma, T, n_steps, n_paths, seed=None, antithetic=False
):
    """
    Simule des trajectoires MBG (log-normal) pour un sous-jacent.
    Peut utiliser les variates antithétiques pour réduire la variance.
    """

    if n_steps <= 0 or n_paths <= 0:
        raise ValueError("n_steps and n_paths must be positive integers.")

    if seed is not None:
        np.random.seed(seed)

    dt = T / n_steps

    # --- Variates antithétiques ---
    if antithetic:
        if n_paths % 2 != 0:
            raise ValueError("n_paths must be even when using antithetic variates.")
        half = n_paths // 2
        Z = np.random.normal(size=(half, n_steps))
        Z = np.vstack([Z, -Z])
    else:
        Z = np.random.normal(size=(n_paths, n_steps))

    increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    log_paths = np.cumsum(increments, axis=1)
    S_paths = S0 * np.exp(log_paths)

    # Ajout de S0 au début
    S_paths = np.concatenate([np.full((n_paths, 1), S0), S_paths], axis=1)

    return S_paths


def monte_carlo_pricer(S_paths, payoff, r, T, return_discounted=False):
    """
    Pricer Monte Carlo générique.
    """
    payoffs = payoff(S_paths[:, -1])
    discounted = np.exp(-r * T) * payoffs

    price = np.mean(discounted)
    stderr = np.std(discounted) / np.sqrt(len(discounted))

    if return_discounted:
        return price, stderr, discounted
    return price, stderr


def price_option_mc(
    S0, K, r, T, sigma, n_steps, n_paths,
    option_type="call", seed=None, antithetic=False,
    return_paths=False
):
    """
    Pricer Monte Carlo complet pour une option européenne.
    """

    if option_type == "call":
        payoff = european_call(K)
    elif option_type == "put":
        payoff = european_put(K)
    else:
        raise ValueError("option_type must be 'call' or 'put'.")

    paths = simulate_gbm_paths(
        S0, r, sigma, T, n_steps, n_paths, seed, antithetic=antithetic
    )

    price, stderr = monte_carlo_pricer(paths, payoff, r, T)

    if return_paths:
        return price, stderr, paths

    return price, stderr

import numpy as np
from scipy.stats import norm

def mc_confidence_interval(payoffs, confidence=0.95):
    """
    Calcule un intervalle de confiance pour un estimateur Monte Carlo.
    """
    mean = np.mean(payoffs)
    std = np.std(payoffs, ddof=1)
    n = len(payoffs)

    z = norm.ppf(0.5 + confidence / 2)
    half_width = z * std / np.sqrt(n)

    return mean - half_width, mean + half_width
