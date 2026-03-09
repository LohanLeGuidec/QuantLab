import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import numpy as np

from .._03_Risk.drawdown import compute_drawdown

plt.style.use("seaborn-v0_8-darkgrid")


# ============================================================
# 1) PLOT DU TICKER (PROFESSIONNEL)
# ============================================================

def plot_ticker(ticker, save=False, filename="ticker_plot.png"):
    """
    Graphique professionnel :
    - Prix + SMA20 + SMA50
    - Volume
    - Volatilité réalisée (20 jours)
    """

    # -----------------------------
    # 📌 Chargement des données
    # -----------------------------
    data = yf.Ticker(ticker)
    hist = data.history(period="1y")

    if hist.empty:
        raise ValueError(f"Aucune donnée trouvée pour {ticker}")

    hist.index = pd.to_datetime(hist.index, errors="coerce")
    hist.index = hist.index.tz_localize(None)

    # -----------------------------
    # 📌 Calcul des indicateurs
    # -----------------------------
    hist["SMA20"] = hist["Close"].rolling(20).mean()
    hist["SMA50"] = hist["Close"].rolling(50).mean()

    hist["returns"] = hist["Close"].pct_change()
    hist["realized_vol"] = hist["returns"].rolling(20).std() * np.sqrt(252)

    # -----------------------------
    # 📌 Layout
    # -----------------------------
    fig = plt.figure(figsize=(14, 9))

    # 1. Prix
    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax1.plot(hist.index, hist["Close"], label="Close", color="white", linewidth=1.5)
    ax1.plot(hist.index, hist["SMA20"], label="SMA 20", color="cyan", linewidth=1)
    ax1.plot(hist.index, hist["SMA50"], label="SMA 50", color="orange", linewidth=1)

    ax1.set_title(f"Évolution du prix de {ticker} (1 an)", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Prix")
    ax1.legend(loc="upper left")

    # 2. Volume
    ax2 = plt.subplot2grid((3, 1), (2, 0))
    ax2.bar(hist.index, hist["Volume"], color="grey", alpha=0.4)
    ax2.set_ylabel("Volume")

    # 3. Volatilité réalisée (overlay)
    ax3 = ax2.twinx()
    ax3.plot(hist.index, hist["realized_vol"], color="red", linewidth=1.2,
             label="Vol. réalisée (20j)")
    ax3.set_ylabel("Volatilité")
    ax3.legend(loc="upper right")

    plt.tight_layout()

    if save:
        fig.savefig(filename, dpi=300)

    plt.show()


# ============================================================
# 2) TRAJECTOIRES MONTE CARLO
# ============================================================

def plot_paths(paths, n=20):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(paths[:, :n], alpha=0.7)
    ax.set_title("Trajectoires simulées (GBM)")
    ax.set_xlabel("Pas de temps")
    ax.set_ylabel("Prix simulé")
    ax.grid(True, alpha=0.3)
    return fig

# ============================================================
# 3) DISTRIBUTION DES PAYOFFS
# ============================================================

def plot_payoff_distribution(discounted):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(discounted, bins=50, color="#4C72B0", alpha=0.8, edgecolor="white")
    ax.set_title("Distribution des payoffs actualisés")
    ax.set_xlabel("Payoff actualisé")
    ax.set_ylabel("Fréquence")
    ax.grid(True, alpha=0.3)
    return fig


# ============================================================
# 4) COURBE DE CONVERGENCE MONTE CARLO
# ============================================================

def plot_convergence(n_list, prices, bs_price=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(n_list, prices, marker="o", label="Prix Monte Carlo", color="#4C72B0")

    if bs_price is not None:
        ax.axhline(bs_price, color="#C44E52", linestyle="--", linewidth=2, label="Prix Black-Scholes")

    ax.set_title("Convergence du prix Monte Carlo")
    ax.set_xlabel("Nombre de trajectoires")
    ax.set_ylabel("Prix estimé")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig


def plot_drawdown(drawdown):
    plt.figure(figsize=(10,4))
    plt.plot(drawdown, label="Drawdown")
    plt.axhline(0, color="black", linewidth=1)
    plt.title("Drawdown du sous-jacent")
    plt.grid(True)
    plt.legend()
    plt.show()