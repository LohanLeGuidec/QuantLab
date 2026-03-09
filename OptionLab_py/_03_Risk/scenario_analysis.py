from .._02_Pricing.blackandscholes import black_scholes


def scenario_analysis(S, K, r, T, sigma, option_type):
    """
    Quelques scénarios de marché stylisés.
    """
    scenarios = {
        "Crash -20%": (S * 0.8, sigma * 1.5),
        "Rally +15%": (S * 1.15, sigma * 0.9),
        "Volatility Spike": (S, sigma * 1.8),
        "Volatility Crush": (S, sigma * 0.7),
    }

    results = {}
    for name, (S_scen, sigma_scen) in scenarios.items():
        price = black_scholes(S_scen, K, r, T, sigma_scen, option_type)
        results[name] = price

    return results