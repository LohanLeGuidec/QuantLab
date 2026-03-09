import streamlit as st
import matplotlib.pyplot as plt

from OptionLab_py._01_dataloader import (
    price, sigma_bs, risk_free_rate, get_region_from_ticker
)
from OptionLab_py._05_strategies.strategy_optimizer import StrategyOptimizer
from OptionLab_py._05_strategies.utils import auto_offset
from OptionLab_py._05_strategies.optimization_presets import build_optimization_grid


def run():
    st.title("⚙️ Optimisation de stratégies")

    ticker = st.text_input("Ticker", "AAPL")
    T = st.number_input("Maturité (années)", value=1.0, step=0.1)
    K = st.number_input("Strike central", value=150.0, step=1.0)

    S = price(ticker)
    region = get_region_from_ticker(ticker)
    r = risk_free_rate(region)
    sigma = sigma_bs(ticker)

    with st.expander("Paramètres de marché détectés automatiquement"):
        st.write(f"Spot : **{S:.2f}**")
        st.write(f"Région : **{region}**")
        st.write(f"Taux sans risque : **{r:.4f}**")
        st.write(f"Volatilité historique : **{sigma:.4f}**")

    offset = auto_offset(S)
    st.info(f"Offset automatique utilisé : **{offset}** points")

    if st.button("Lancer l’optimisation"):

        optimizer = StrategyOptimizer(S, r, T, sigma)

        optimizations = build_optimization_grid(K, offset)

        df, best_strategies = optimizer.run_all(optimizations)

        for name, info in best_strategies.items():
            st.markdown("---")
            st.subheader(info["title"])

            st.write("**Meilleurs paramètres :**", info["params"])
            st.write("**Score :**", info["score"])
            st.json(info["analysis"])

            fig = info["strategy"].plot()
            st.pyplot(fig)

        st.markdown("## 📊 Tableau comparatif final")
        st.dataframe(df)

        st.markdown("## 🏆 Classement des stratégies")
        st.dataframe(optimizer.rank(df))

        st.markdown("## 📈 Radar Chart – Profil de risque")
        fig_radar = optimizer.radar_chart(df)
        st.pyplot(fig_radar)

    st.markdown("---")
    st.markdown("Développé par **Lohan Le Guidec** – M1 MBFA, Parcours Ingénierie Economique et Financière, Université de Rennes")