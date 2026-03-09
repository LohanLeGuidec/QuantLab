import numpy as np
import pandas as pd
from OptionLab_py._01_dataloader import load_prices, compute_returns
import pandas as pd
import numpy as np
import yfinance as yf

def get_currency_from_ticker(ticker : str) -> str:
    if ticker.endswith('.USD'):
        return 'USD'
    elif ticker.endswith('.EUR'):
        return 'EUR'
    elif ticker.endswith('.L'):
        return 'GBP'
    elif ticker.endswith('.JPY'):
        return 'JPY'
    elif ticker.endswith('.CHF'):
        return 'CHF'
    elif ticker.endswith('.CAD'):
        return 'CAD'
    elif ticker.endswith('.AX'):
        return 'AUD'
    elif ticker.endswith('.IN'):
        return 'INR'
    elif ticker.endswith('.SA'):
        return 'BRL'
    else:
        return 'USD'  # Par défaut
    
def get_benchmark_ticker_from_currency(currency: str) -> str:
    if currency == "EUR":
        return "^STOXX50E"   # Euro Stoxx 50
    elif currency == "USD":
        return "^GSPC"       # S&P 500
    elif currency == "GBP":
        return "^FTSE"       # FTSE 100
    elif currency == "JPY":
        return "^N225"       # Nikkei 225
    elif currency == "CHF":
        return "^SSMI"       # Swiss Market Index
    elif currency == "CAD":
        return "^GSPTSE"     # S&P/TSX Composite
    elif currency == "AUD":
        return "^AXJO"       # S&P/ASX 200
    elif currency == "CNY":
        return "000001.SS"   # Shanghai Composite
    elif currency == "INR":
        return "^NSEI"       # Nifty 50
    elif currency == "BRL":
        return "^BVSP"       # Bovespa
    else:
        raise ValueError("Devise non supportée")

BENCHMARK_NAMES = {
    "^GSPC": "S&P 500",
    "^STOXX50E": "Euro Stoxx 50",
    "^FTSE": "FTSE 100",
    "^N225": "Nikkei 225",
    "^SSMI": "Swiss Market Index",
    "^GSPTSE": "S&P/TSX Composite",
    "^AXJO": "S&P/ASX 200",
    "000001.SS": "Shanghai Composite",
    "^NSEI": "Nifty 50",
    "^BVSP": "Bovespa"
}

def map_tickers_to_benchmarks(tickers: list[str]) -> dict[str, str]:
    return {
        ticker: get_benchmark_ticker_from_currency(get_currency_from_ticker(ticker))
        for ticker in tickers
    }

def beta_auto_for_all(
    ticker: str,
    start_date: str = "2020-01-01"
):
    # 1) Trouver la devise du ticker
    currency = get_currency_from_ticker(ticker)

    # 2) Trouver le benchmark associé
    benchmark = get_benchmark_ticker_from_currency(currency)
    benchmark_name = BENCHMARK_NAMES.get(benchmark, benchmark)

    # 3) Télécharger les prix du ticker
    prices = yf.download(ticker, start=start_date)["Close"]

    # 4) Télécharger les prix du benchmark
    benchmark_prices = load_prices([benchmark], start=start_date)[benchmark]

    # 5) Calcul des rendements
    asset_returns = prices.pct_change().dropna()
    bench_returns = benchmark_prices.pct_change().dropna()

    # 6) Alignement strict
    aligned = pd.concat([asset_returns, bench_returns], axis=1, join="inner").dropna()
    asset = aligned.iloc[:, 0]
    bench = aligned.iloc[:, 1]

    # 7) Calcul du bêta
    covariance = np.cov(asset, bench)[0, 1]
    variance = np.var(bench)
    beta = covariance / variance

    return beta, benchmark_name

def rolling_beta(
    ticker: str,
    window: int = 30,
    start_date: str = "2020-01-01"
):
    import yfinance as yf

    # 1) Devise → benchmark
    currency = get_currency_from_ticker(ticker)
    benchmark = get_benchmark_ticker_from_currency(currency)

    # 2) Télécharger les prix
    data = yf.download([ticker, benchmark], start=start_date)["Close"].dropna()

    # 3) Calcul des rendements
    returns = data.pct_change().dropna()

    # 4) Rolling covariance et variance
    cov = returns[ticker].rolling(window).cov(returns[benchmark])
    var = returns[benchmark].rolling(window).var()

    # 5) Rolling beta
    beta_roll = cov / var

    return beta_roll, benchmark