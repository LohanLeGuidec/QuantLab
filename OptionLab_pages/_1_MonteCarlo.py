import streamlit as st
import matplotlib.pyplot as plt

from OptionLab_py._01_dataloader import (
    price, sigma_bs, risk_free_rate, get_region_from_ticker,
)
from OptionLab_py._02_Pricing import (
    monte_carlo_pricer, 
    simulate_gbm_paths,
    european_call,
    european_put,
    price_option_mc
)
from OptionLab_py._02_Pricing.blackandscholes import black_scholes

from OptionLab_py._04_utils import (
    plot_paths,
    plot_payoff_distribution,
    plot_convergence
)

def run():
    st.title("🎲 Pricing Monte Carlo")
    
    st.markdown("""
    ### 🧠 Comment fonctionne le pricing Monte Carlo ?

    Le pricing Monte Carlo consiste à estimer le prix d’une option en simulant un grand nombre 
    de trajectoires possibles du sous-jacent, selon un mouvement brownien géométrique (GBM).  
    Pour chaque trajectoire, on calcule le payoff de l’option à maturité, puis on actualise 
    et on fait la moyenne.

    Cette méthode est particulièrement utile lorsque :
    - la formule de Black‑Scholes n’est pas applicable (options exotiques, payoffs complexes),
    - on veut visualiser l’incertitude du prix,
    - on souhaite analyser la convergence statistique du modèle.

    Dans le cas d’une option européenne simple, Monte Carlo doit converger vers le prix 
    analytique de Black‑Scholes, ce qui permet de valider la simulation.
    """)
    # ---------------------------------------------------------
    # 1) Paramètres utilisateur
    # ---------------------------------------------------------
    ticker = st.text_input("Ticker", "AAPL")
    option_type = st.selectbox("Type d’option", ["call", "put"])
    K = st.number_input("Strike", value=150.0, step=1.0, format="%.2f")
    T = st.number_input("Maturité (années)", value=1.0, step=0.1, format="%.2f")
    n_paths = st.number_input("Nombre de trajectoires", value=50000, step=1000)
    n_steps = st.number_input("Nombre de pas", value=252, step=10)

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

    # ---------------------------------------------------------
    # 3) Simulation Monte Carlo
    # ---------------------------------------------------------
    if st.button("Lancer la simulation"):

        st.subheader("Résultat Monte Carlo")

        price_mc, stderr_mc = price_option_mc(
            S0=S, K=K, r=r, T=T, sigma=sigma,
            n_steps=int(n_steps), n_paths=int(n_paths),
            option_type=option_type, seed=42, antithetic=True
        )

        st.write(f"**Prix MC :** {price_mc:.4f}")
        st.write(f"**Erreur standard :** {stderr_mc:.6f}")

        # Intervalle de confiance 95%
        ci_low = price_mc - 1.96 * stderr_mc
        ci_high = price_mc + 1.96 * stderr_mc
        st.write(f"**Intervalle de confiance 95% :** [{ci_low:.4f}, {ci_high:.4f}]")

        bs_price = black_scholes(S, K, r, T, sigma, option_type)
        st.write(f"**Prix Black-Scholes :** {bs_price:.4f}")

        # ---------------------------------------------------------
        # 4) Graphiques
        # ---------------------------------------------------------

        # --- Trajectoires simulées ---
        st.subheader("Trajectoires simulées")
        paths = simulate_gbm_paths(S, r, sigma, T, int(n_steps), 200, seed=42)
        fig1 = plot_paths(paths, n=20)
        st.pyplot(fig1)

        # --- Distribution des payoffs ---
        st.subheader("Distribution des payoffs")
        _, _, discounted = monte_carlo_pricer(
            paths,
            european_call(K) if option_type == "call" else european_put(K),
            r, T, return_discounted=True
        )
        fig2 = plot_payoff_distribution(discounted)
        st.pyplot(fig2)

        # --- Convergence ---
        st.subheader("Convergence")
        n_list = [1_000, 5_000, 10_000, 20_000, 50_000]

        prices = [
            price_option_mc(
                S0=S, K=K, r=r, T=T, sigma=sigma,
                n_steps=int(n_steps), n_paths=n,
                option_type=option_type
            )[0]
            for n in n_list
        ]

        fig3 = plot_convergence(n_list, prices, bs_price=bs_price)
        st.pyplot(fig3)

    st.markdown("---")
    st.markdown("Développé par **Lohan Le Guidec** – M1 MBFA, Parcours Ingénierie Economique et Financière, Université de Rennes")