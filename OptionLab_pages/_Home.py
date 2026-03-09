from matplotlib import ticker
import streamlit as st
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

from OptionLab_py._01_dataloader import (
    price, sigma_bs, risk_free_rate, get_region_from_ticker, compute_returns
)
from OptionLab_py._03_Risk import (
    beta_auto_for_all, 
    rolling_beta
)


def run():
    st.title("📊 OptionLab – Dashboard")

    st.markdown("""
    ### Suite d’outils quantitatifs pour le pricing, les stratégies et le risk management

    OptionLab regroupe plusieurs modules professionnels :
    - **Pricing Black–Scholes**
    - **Volatilité implicite**
    - **Monte Carlo**
    - **Stratégies optionnelles**
    - **Optimisation de stratégies**
    - **Analyse du risque**
    - **Backtesting**

    Utilisez le menu de gauche pour naviguer entre les modules.
    """)

    # ---------------------------------------------------------
    # 1) Input utilisateur
    # ---------------------------------------------------------
    ticker = st.text_input("Ticker", "AAPL")
    S = price(ticker)
    sigma = sigma_bs(ticker)
    r = risk_free_rate(get_region_from_ticker(ticker))
    
    # ---------------------------------------------------------
    # 2) Indicateurs clés du marché
    # ---------------------------------------------------------
    st.subheader("📌 Indicateurs clés du marché")

    # --- Variation journalière ---
    data_full = yf.download(ticker, period="2d")[["Close"]].dropna()
    if len(data_full) >= 2:
        daily_return = float((data_full.iloc[-1] / data_full.iloc[-2] - 1) * 100)
    else:
        daily_return = 0.0

    # --- Volatilité réalisée (20 jours) ---
    data_1y = yf.download(ticker, period="1y")[["Close"]].dropna()
    returns_1y = compute_returns(data_1y)
    realized_vol = float(returns_1y.iloc[:, 0].rolling(20).std().iloc[-1] * np.sqrt(252))

    # --- Max Drawdown (1 an) ---
    series_1y = data_1y["Close"]
    rolling_max = series_1y.cummax()
    drawdown = (series_1y - rolling_max) / rolling_max
    max_dd = float(drawdown.min() * 100)

    # --- Beta ---
    beta_value, benchmark_name = beta_auto_for_all(ticker)
    beta_value = float(beta_value)

    # --- Sharpe ratio ---
    prices = yf.download(ticker, start="2020-01-01")[["Close"]].dropna()
    returns = compute_returns(prices)
    ret = returns.iloc[:, 0]
    sharpe = float(ret.mean() / ret.std() * np.sqrt(252))

    # ---------------------------------------------------------
    # 3) Mise en page des indicateurs
    # ---------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Spot", f"{S:.2f}")
        st.metric("📈 Variation journalière", f"{daily_return:+.2f}%")

    with col2:
        st.metric("📊 Vol historique (BS)", f"{sigma:.4f}")
        st.metric("📉 Vol réalisée (20j)", f"{realized_vol:.4f}")

    with col3:
        st.metric("📉 Max Drawdown (1 an)", f"{max_dd:.2f}%")
        st.metric(f"📌 Beta vs {benchmark_name}", f"{beta_value:.4f}")

    with col4:
        st.metric("⚖️ Sharpe ratio", f"{sharpe:.4f}")
        st.metric("🏦 Taux sans risque", f"{r:.4f}")

    # ---------------------------------------------------------
    # 4) Rolling Beta (30 jours)
    # ---------------------------------------------------------
    st.subheader(f"📉 Rolling Beta (30 jours) – par rapport à {benchmark_name}")

    beta_roll, benchmark = rolling_beta(ticker)

    fig, ax = plt.subplots()
    ax.plot(beta_roll, color="purple")
    ax.axhline(1, color="black", linestyle="--", linewidth=1, alpha=0.6)
    ax.set_title(f"Rolling Beta (30 jours) – {ticker} vs {benchmark}")
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    # ---------------------------------------------------------
    # 5) Graphique du prix sur 1 an
    # ---------------------------------------------------------
    st.subheader("📈 Prix du sous-jacent (1 an)")

    data = yf.download(ticker, period="1y")["Close"]

    fig, ax = plt.subplots()
    ax.plot(data, label=ticker, color="steelblue")
    ax.set_title(f"Évolution du prix – {ticker}")
    ax.set_ylabel("Prix")
    ax.grid(alpha=0.3)

    st.pyplot(fig)

    st.markdown("---")
    st.markdown("Développé par **Lohan Le Guidec** – M1 MBFA, Parcours Ingénierie Economique et Financière, Université de Rennes 1")