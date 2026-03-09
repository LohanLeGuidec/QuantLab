import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

from OptionLab_py._01_dataloader import (
    price, sigma_bs, risk_free_rate, get_region_from_ticker,
)
from OptionLab_py._02_Pricing import (
    black_scholes, compute_greeks
)
from OptionLab_py._03_Risk import (
    compute_drawdown, scenario_analysis, stress_test_price,
    historical_var, historical_cvar
)
from OptionLab_py._04_utils import (
    plot_drawdown
)

def run():
    st.title("🚨 Analyse du risque")

    # ---------------------------------------------------------
    # 1) Paramètres utilisateur
    # ---------------------------------------------------------
    ticker = st.text_input("Ticker", "AAPL")
    option_type = st.selectbox("Type d’option", ["call", "put"])
    K = st.number_input("Strike", value=150.0, step=1.0, format="%.2f")
    T = st.number_input("Maturité (années)", value=1.0, step=0.1, format="%.2f")

    # ---------------------------------------------------------
    # 2) Paramètres de marché détectés automatiquement
    # ---------------------------------------------------------
    S = price(ticker)
    region = get_region_from_ticker(ticker)
    r = risk_free_rate(region)
    sigma = sigma_bs(ticker)

    with st.expander("Paramètres de marché détectés automatiquement"):
        st.write(f"Spot : **{S:.2f}**")
        st.write(f"Région : **{region}**")
        st.write(f"Taux sans risque : **{r:.4f}**")
        st.write(f"Volatilité historique : **{sigma:.4f}**")

    if st.button("Analyser le risque"):

        # ---------------------------------------------------------
        # 3) Greeks (sensibilités)
        # ---------------------------------------------------------
        st.subheader("Greeks (sensibilités)")

        greeks = compute_greeks(S, K, r, T, sigma, option_type)
        for greek, value in greeks.items():
            st.write(f"**{greek}** : {value:.6f}")

        # ---------------------------------------------------------
        # 4) Données historiques
        # ---------------------------------------------------------
        data = yf.download(ticker, period="1y")["Close"]
        returns = data.pct_change().dropna()

        # ---------------------------------------------------------
        # 5) VaR & CVaR
        # ---------------------------------------------------------
        st.subheader("VaR & CVaR historiques (95%)")

        var_95 = float(historical_var(returns, alpha=0.05))
        cvar_95 = float(historical_cvar(returns, alpha=0.05))

        st.write(f"**VaR 95% :** {var_95:.4f}")
        st.write(f"**CVaR 95% :** {cvar_95:.4f}")

        # ---------------------------------------------------------
        # 6) Stress Test Delta (S ± 2%, ±5%)
        # ---------------------------------------------------------
        st.subheader("Stress Test Delta (chocs sur le spot)")

        shocks_S = [-0.05, -0.02, 0.02, 0.05]
        delta_results = {}

        for shock in shocks_S:
            new_S = S * (1 + shock)
            new_price = black_scholes(new_S, K, r, T, sigma, option_type)
            delta_results[f"S {shock*100:+.0f}%"] = new_price

        st.json(delta_results)

        # ---------------------------------------------------------
        # 7) Stress Test Vega (σ ± 10%, ±20%)
        # ---------------------------------------------------------
        st.subheader("Stress Test Vega (chocs sur la volatilité)")

        shocks_sigma = [-0.10, -0.20, 0.10, 0.20]
        vega_results = {}

        for shock in shocks_sigma:
            new_sigma = sigma * (1 + shock)
            new_price = black_scholes(S, K, r, T, new_sigma, option_type)
            vega_results[f"σ {shock*100:+.0f}%"] = new_price

        st.json(vega_results)

        # ---------------------------------------------------------
        # 8) Stress tests complets (ton module)
        # ---------------------------------------------------------
        st.subheader("Stress tests (module interne)")

        stress = stress_test_price(
            S=S, K=K, r=r, T=T, sigma=sigma,
            option_type=option_type
        )
        st.json(stress)

        # ---------------------------------------------------------
        # 9) Scénarios stylisés
        # ---------------------------------------------------------
        st.subheader("Scénarios stylisés")

        scen_results = scenario_analysis(S, K, r, T, sigma, option_type)
        st.json(scen_results)

        # ---------------------------------------------------------
        # 10) Histogramme des rendements
        # ---------------------------------------------------------
        st.subheader("Distribution des rendements historiques")

        fig_hist, ax = plt.subplots()
        ax.hist(returns, bins=40, alpha=0.7, color="steelblue")
        ax.set_title("Histogramme des rendements")
        st.pyplot(fig_hist)

        # ---------------------------------------------------------
        # 11) Rolling Volatility (20 jours)
        # ---------------------------------------------------------
        st.subheader("Volatilité glissante (20 jours)")

        rolling_vol = returns.rolling(20).std() * (252**0.5)

        fig_vol, ax = plt.subplots()
        ax.plot(rolling_vol, color="darkorange")
        ax.set_title("Volatilité glissante (20 jours)")
        st.pyplot(fig_vol)

        # ---------------------------------------------------------
        # 12) Drawdown
        # ---------------------------------------------------------
        st.subheader("Drawdown du sous-jacent")

        drawdown, max_dd = compute_drawdown(data)
        max_dd_val = float(max_dd.iloc[0]) if hasattr(max_dd, "iloc") else float(max_dd)

        st.write(f"**Max Drawdown :** {max_dd_val:.4f}")

        fig = plot_drawdown(drawdown)
        st.pyplot(fig if fig is not None else plt.gcf())
    
    st.markdown("---")
    st.markdown("Développé par **Lohan Le Guidec** – M1 MBFA, Parcours Ingénierie Economique et Financière, Université de Rennes")