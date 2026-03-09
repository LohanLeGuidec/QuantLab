from .._02_Pricing.blackandscholes import black_scholes


def stress_test_price(S, K, r, T, sigma, option_type, dS=0.05, dSigma=0.02, dR=0.01):
    """
    Stress tests simples :
    - choc sur le sous-jacent (+/- dS)
    - choc sur la volatilité (+/- dSigma)
    - choc sur le taux (+/- dR)
    """

    base = black_scholes(S, K, r, T, sigma, option_type)

    scenarios = {
        "Base": base,
        "S +5%": black_scholes(S*(1+dS), K, r, T, sigma, option_type),
        "S -5%": black_scholes(S*(1-dS), K, r, T, sigma, option_type),
        "Vol +2%": black_scholes(S, K, r, T, sigma+dSigma, option_type),
        "Vol -2%": black_scholes(S, K, r, T, sigma-dSigma, option_type),
        "Taux +1%": black_scholes(S, K, r+dR, T, sigma, option_type),
        "Taux -1%": black_scholes(S, K, r-dR, T, sigma, option_type),
    }

    return scenarios

def stress_test_(S, K, r, T, sigma, option_type,
                shocks_S=[-0.05, 0.05],
                shocks_sigma=[-0.02, 0.02],
                shocks_r=[-0.01, 0.01]):
    """
    Stress test générique : applique plusieurs chocs sur S, sigma et r.
    """
    results = {}

    base = black_scholes(S, K, r, T, sigma, option_type)
    results["Base"] = base

    for dS in shocks_S:
        results[f"S {dS:+.0%}"] = black_scholes(S*(1+dS), K, r, T, sigma, option_type)

    for dV in shocks_sigma:
        results[f"Vol {dV:+.0%}"] = black_scholes(S, K, r, T, sigma+dV, option_type)

    for dR in shocks_r:
        results[f"Taux {dR:+.0%}"] = black_scholes(S, K, r+dR, T, sigma, option_type)

    return results