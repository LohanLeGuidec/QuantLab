import numpy as np

def historical_var(returns, alpha=0.05):
    """
    VaR historique à un niveau alpha.
    returns : série de rendements journaliers
    """
    return np.percentile(returns, 100 * alpha)

def historical_cvar(returns, alpha=0.05):
    """
    CVaR historique (Expected Shortfall).
    """
    var = historical_var(returns, alpha)
    return returns[returns <= var].mean()

def var_(returns, alpha=0.05):
    """
    VaR paramétrique (variance-covariance).
    Hypothèse : rendements ~ N(mu, sigma)
    """
    mu = np.mean(returns)
    sigma = np.std(returns, ddof=1)

    # Quantile normal
    from scipy.stats import norm
    z = norm.ppf(alpha)

    return mu + z * sigma