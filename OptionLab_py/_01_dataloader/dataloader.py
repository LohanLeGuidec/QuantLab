import yfinance as yf
import pandas as pd
import numpy as np

def load_prices(tickers, start=None, end=None):
    data = yf.download(tickers, start=start, end=end, progress=False)

    # Si MultiIndex → on prend le niveau "Adj Close"
    if isinstance(data.columns, pd.MultiIndex):
        if "Adj Close" in data.columns.levels[0]:
            return data["Adj Close"]
        else:
            # fallback si Adj Close absent
            return data["Close"]

    # Si SingleIndex → on vérifie la présence de Adj Close
    if "Adj Close" in data.columns:
        return data["Adj Close"]

    # fallback final
    if "Close" in data.columns:
        return data["Close"]

    raise ValueError("Impossible de trouver Adj Close ou Close dans les données téléchargées.")

import yfinance as yf

def price(ticker):
    data = yf.Ticker(ticker)
    S = data.history(period="1d")["Close"].iloc[-1]
    print(f"Prix actuel de {ticker} : {S:.2f}")
    return S

def compute_returns(prices: pd.DataFrame, log=False) -> pd.DataFrame:
    
    # Calcul les rendements simple ou logarithmiques des prix.

    if log:
        returns = np.log(prices / prices.shift(1))
    else:
        returns = prices.pct_change()
    return returns.dropna()

