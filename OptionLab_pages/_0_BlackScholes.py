import streamlit as st
from OptionLab_py._01_dataloader import (
    price,
    risk_free_rate,
    get_region_from_ticker,
    sigma_bs
)
from OptionLab_py._02_Pricing import (
    black_scholes,
    compute_greeks
)

def run():
    st.title("📘 Pricing Black–Scholes")

    # ---------------------------------------------------------
    # 1) Paramètres utilisateur
    # ---------------------------------------------------------
    ticker = st.text_input("Ticker", "AAPL")
    option_type = st.selectbox("Type d'option", ["call", "put"])
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

    if st.button("Calculer le prix BS"):

        # ---------------------------------------------------------
        # 3) Résultats Black–Scholes
        # ---------------------------------------------------------
        st.subheader("Résultats Black–Scholes")

        price_bs = black_scholes(S, K, r, T, sigma, option_type)
        st.write(f"**Prix théorique :** {price_bs:.4f}")

        # ---------------------------------------------------------
        # 4) Greeks
        # ---------------------------------------------------------
        st.subheader("Greeks")

        greeks = compute_greeks(S, K, r, T, sigma, option_type)
        for greek, value in greeks.items():
            st.write(f"**{greek}** : {value:.6f}")

    st.markdown("---")
    st.markdown("Développé par **Lohan Le Guidec** – M1 MBFA, Parcours Ingénierie Economique et Financière, Université de Rennes")