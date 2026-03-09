import streamlit as st
import matplotlib.pyplot as plt
from OptionLab_py._01_dataloader import (
    price, sigma_bs, risk_free_rate, get_region_from_ticker,
)


from OptionLab_py._05_strategies.backtest import backtest_strategy


def run():
    st.title("📈 Backtest de stratégies optionnelles")

    st.markdown("""
    Cette page permet de backtester plusieurs stratégies :
    - Straddle  
    - Strangle  
    - Bull Call Spread  
    - Bear Put Spread  
    - Butterfly  
    - Iron Condor  
    """)

    st.markdown("""
    ### 🧠 Comment fonctionne le backtest ?

    Le backtest consiste à appliquer une stratégie optionnelle sur des données historiques
    pour analyser son comportement réel : PnL, drawdown, Sharpe, stabilité, sensibilité au marché.
    Chaque jour, la stratégie est revalorisée avec les paramètres de marché correspondants.
    """)

    ticker = st.text_input("Ticker", "AAPL")
    maturity = st.slider("Maturité (jours)", 10, 365, 30)
    strike = st.number_input("Strike central (K)", value=100.0)

    strategie = st.selectbox(
        "Stratégie",
        [
            "Straddle",
            "Strangle",
            "Bull Call Spread",
            "Bear Put Spread",
            "Butterfly",
            "Iron Condor",
        ],
    )

    # Paramètres de marché détectés automatiquement
    S = price(ticker)
    region = get_region_from_ticker(ticker)
    r = risk_free_rate(region)
    sigma = sigma_bs(ticker)

    with st.expander("Paramètres de marché détectés automatiquement"):
        st.write(f"Spot : **{S:.2f}**")
        st.write(f"Région : **{region}**")
        st.write(f"Taux sans risque : **{r:.4f}**")
        st.write(f"Volatilité historique : **{sigma:.4f}**")


    # Paramètres dynamiques selon la stratégie
    if strategie in ["Bull Call Spread", "Bear Put Spread"]:
        width = st.number_input("Écart entre strikes", value=10.0)
    elif strategie == "Strangle":
        width = st.number_input("Écart entre K1 et K2", value=10.0)
    elif strategie == "Butterfly":
        width = st.number_input("Écart K2-K1 et K3-K2", value=10.0)
    elif strategie == "Iron Condor":
        width = st.number_input("Écart entre strikes successifs", value=10.0)
    else:
        width = None
    
    if st.button("Lancer le backtest"):
        # Mapping vers StrategyFactory
        if strategie == "Straddle":
            params = {"K": strike}
            strat_name = "straddle"

        elif strategie == "Strangle":
            params = {"K1": strike - width, "K2": strike + width}
            strat_name = "strangle"

        elif strategie == "Bull Call Spread":
            params = {"K1": strike, "K2": strike + width}
            strat_name = "bull_call"

        elif strategie == "Bear Put Spread":
            params = {"K1": strike, "K2": strike - width}
            strat_name = "bear_put"

        elif strategie == "Butterfly":
            params = {"K1": strike - width, "K2": strike, "K3": strike + width}
            strat_name = "butterfly"

        elif strategie == "Iron Condor":
            params = {
                "K1": strike - 2 * width,
                "K2": strike - width,
                "K3": strike + width,
                "K4": strike + 2 * width,
            }
            strat_name = "iron_condor"

        # Lancement du backtest
        results = backtest_strategy(
            strategy_name=strat_name,
            ticker=ticker,
            maturity_days=maturity,
            **params
        )

        pnl = results["pnl_series"]
        
        st.subheader("📉 Évolution du sous-jacent")
        fig2, ax2 = plt.subplots()
        ax2.plot(results["underlying"], color="gray")
        ax2.set_title("Sous-jacent")
        ax2.grid(alpha=0.3)
        st.pyplot(fig2)

        st.subheader("📊 PnL de la stratégie")
        fig, ax = plt.subplots()
        ax.plot(pnl, color="#4C72B0")
        ax.axhline(0, color="black", linewidth=1)
        ax.set_title("Évolution du PnL")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

        col1, col2, col3 = st.columns(3)
        col1.metric("PnL final", f"{results['pnl_final']:.2f}")
        col2.metric("Sharpe ratio", f"{results['sharpe']:.2f}")
        col3.metric("Max Drawdown", f"{results['max_drawdown']:.2f}%")
    
    
    st.markdown("---")
    st.markdown("Développé par **Lohan Le Guidec** – M1 MBFA, Parcours Ingénierie Economique et Financière, Université de Rennes")