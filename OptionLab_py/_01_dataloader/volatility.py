import yfinance as yf
import numpy as np

def sigma_bs(ticker):
    data = yf.Ticker(ticker)
    sigma = data.history(period="1y")["Close"].pct_change().std() * np.sqrt(252)
    print(f"Volatilité historique estimée pour {ticker} : {sigma:.4f}")
    return sigma
