"""
utils_pricing.py
Fonctions utilitaires pour diagnostics, convergence, erreurs, plots et performance.
"""

import numpy as np
import matplotlib.pyplot as plt
import time


# ============================
#   Gestion des seeds
# ============================

def set_seed(seed):
    """Fixe la seed pour la reproductibilité."""
    if seed is not None:
        np.random.seed(seed)


# ============================
#   Intervalles de confiance
# ============================

def mc_confidence_interval(estimates, alpha=0.05):
    """
    Calcule un intervalle de confiance asymptotique pour une série d'estimations MC.
    """
    mean = np.mean(estimates)
    stderr = np.std(estimates) / np.sqrt(len(estimates))
    z = 1.96  # 95%
    return mean - z * stderr, mean + z * stderr


# ============================
#   Erreurs / Comparaisons
# ============================

def relative_error(mc_price, bs_price):
    """Erreur relative entre Monte Carlo et Black-Scholes."""
    return abs(mc_price - bs_price) / bs_price


# ============================
#   Timer pour performance
# ============================

class Timer:
    """Context manager pour mesurer le temps d'exécution."""
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        self.end = time.time()
        self.duration = self.end - self.start


# ============================
#   Diagnostics Monte Carlo
# ============================

def plot_payoff_distribution(discounted_payoffs, bins=50):
    """Histogramme des payoffs actualisés."""
    plt.hist(discounted_payoffs, bins=bins, density=True, alpha=0.7)
    plt.title("Distribution des payoffs actualisés")
    plt.xlabel("Payoff actualisé")
    plt.ylabel("Densité")
    plt.show()


# ============================
#   Courbe de convergence
# ============================

def convergence_curve(pricer, n_paths_list):
    """
    Calcule la convergence du prix MC en fonction du nombre de trajectoires.
    pricer doit être une fonction prenant n_paths en argument.
    """
    prices = []
    for n in n_paths_list:
        price, _ = pricer(n)
        prices.append(price)
    return prices


def plot_convergence(n_paths_list, prices, bs_price=None):
    """Trace la convergence MC."""
    plt.plot(n_paths_list, prices, marker="o", label="Monte Carlo")
    if bs_price is not None:
        plt.axhline(bs_price, color="red", linestyle="--", label="Black-Scholes")
    plt.xlabel("Nombre de trajectoires")
    plt.ylabel("Prix estimé")
    plt.title("Convergence du pricer Monte Carlo")
    plt.legend()
    plt.grid(True)
    plt.show()