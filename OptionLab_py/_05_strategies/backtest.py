import numpy as np
import pandas as pd
import yfinance as yf

from .._01_dataloader import sigma_bs, risk_free_rate, get_region_from_ticker
from .strategy_factory import StrategyFactory


def compute_sharpe(returns):
    if returns.std() == 0:
        return 0.0
    return float(returns.mean() / returns.std() * np.sqrt(252))


def compute_max_drawdown(series):
    """
    Drawdown professionnel : basé sur la valeur de la stratégie,
    avec plancher pour éviter les divisions par zéro.
    """
    rolling_max = series.cummax().clip(lower=1e-6)
    drawdown = (series - rolling_max) / rolling_max
    return float(drawdown.min() * 100)


def backtest_strategy(strategy_name: str, ticker: str, maturity_days: int, **strategy_params):
    """
    Backtest générique basé sur les classes de stratégies (StrategyFactory).
    """
    data = yf.download(ticker, period="1y")["Close"].dropna()
    if len(data) < 30:
        raise ValueError("Pas assez de données pour backtester.")

    region = get_region_from_ticker(ticker)
    r = risk_free_rate(region)

    T = maturity_days / 252
    S0 = float(data.iloc[0])
    sigma0 = sigma_bs(ticker)

    # Instanciation de la stratégie à t=0
    strategy = StrategyFactory.create(
        strategy_name,
        S=S0,
        r=r,
        T=T,
        sigma=sigma0,
        **strategy_params,
    )

    initial_cost = strategy.price()

    values = []
    dates = []

    for i in range(len(data)):
        S_t = float(data.iloc[i])
        t = max(T - i / 252, 0.0001)
        sigma_t = sigma_bs(ticker)

        # Mise à jour dynamique de la volatilité
        strategy.sigma = sigma_t
        price_t = strategy.price_at(S_t, t)

        values.append(price_t)
        dates.append(data.index[i])

    values = pd.Series(values, index=dates)
    returns = values.diff().dropna()

    stats = {
        "pnl_final": float(values.iloc[-1] - initial_cost),
        "sharpe": compute_sharpe(returns),
        "max_drawdown": compute_max_drawdown(values),
        "pnl_series": values,
        "underlying": data,  
    }

    return stats