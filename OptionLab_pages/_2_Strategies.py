import streamlit as st
import matplotlib.pyplot as plt

from OptionLab_py._01_dataloader import (
    risk_free_rate, sigma_bs, price, get_region_from_ticker
)

from OptionLab_py._05_strategies.strategy_factory import StrategyFactory
from OptionLab_py._05_strategies.strategy_descriptions import smart_summary
from OptionLab_py._05_strategies.utils import auto_offset
from OptionLab_py._05_strategies.scoring import score_strategy_by_name, plot_radar

def run():
    st.title("🧩 Stratégies optionnelles")

    col1, col2 = st.columns(2)

    with col1:
        ticker = st.text_input("Ticker", "AAPL")
        T = st.number_input("Maturité (années)", value=1.0, step=0.1)
        K = st.number_input("Strike central", value=150.0, step=1.0)

    with col2:
        strategy_name = st.selectbox(
            "Stratégie",
            ["bull_call", "straddle", "strangle", "butterfly", "iron_condor"]
        )

    S = price(ticker)
    region = get_region_from_ticker(ticker)
    r = risk_free_rate(region)
    sigma = sigma_bs(ticker)

    with st.expander("📊 Paramètres de marché détectés automatiquement"):
        st.write(f"**Spot :** {S:.2f}")
        st.write(f"**Région :** {region}")
        st.write(f"**Taux sans risque :** {r:.4f}")
        st.write(f"**Volatilité historique :** {sigma:.4f}")

    if strategy_name == "bull_call":
        step_opt = st.number_input("Écart entre les strikes", value=5.0, step=1.0)
    else:
        step_opt = auto_offset(S)
        st.info(f"Offset automatique utilisé : **{step_opt}** points")

    if st.button("Analyser la stratégie"):

        params = {
            "bull_call": dict(K1=K, K2=K + step_opt),
            "straddle": dict(K=K),
            "strangle": dict(K1=K - step_opt, K2=K + step_opt),
            "butterfly": dict(K1=K - step_opt, K2=K, K3=K + step_opt),
            "iron_condor": dict(
                K1=K - 2 * step_opt, K2=K - step_opt,
                K3=K + step_opt, K4=K + 2 * step_opt
            ),
        }[strategy_name]

        
        strategy = StrategyFactory.create(
            strategy_name, S=S, r=r, T=T, sigma=sigma, **params
        )

        metrics = strategy.compute_metrics()

        st.subheader("🧠 Résumé de la stratégie")
        st.info(smart_summary(strategy_name))

        st.subheader("📈 Résultats")
        st.json(metrics)

        # --- Scoring ---
        strategy_score = score_strategy_by_name(strategy_name, metrics)

        st.subheader("🏆 Strategy Score")
        st.metric("Score global", f"{strategy_score}/100")

        # Interprétation automatique
        if strategy_score >= 70:
            st.success("Stratégie robuste et bien équilibrée.")
        elif strategy_score >= 50:
            st.info("Stratégie correcte mais améliorable.")
        else:
            st.warning("Stratégie risquée ou peu efficace.")


        st.subheader("📉 Payoff")
        fig = strategy.plot()
        st.pyplot(fig)

        st.subheader("📊 Radar Chart – Profil de la stratégie")
        radar_fig = plot_radar(metrics, strategy_name)
        st.pyplot(radar_fig)

    st.markdown("---")
    st.markdown("Développé par **Lohan Le Guidec** – M1 MBFA, Parcours Ingénierie Economique et Financière, Université de Rennes")