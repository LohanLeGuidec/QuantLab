from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt


class BaseStrategy(ABC):
    """
    Classe de base pour toutes les stratégies d'options.

    Chaque stratégie doit implémenter :
        - payoff(S_T)
        - price()
        - analyze()
        - price_at(S_t, T_t)

    La méthode analyze() doit retourner au minimum les clés suivantes :
        - max_gain        : gain maximal possible
        - max_loss        : perte maximale possible
        - delta           : sensibilité au sous-jacent
        - vega            : sensibilité à la volatilité
        - breakeven_low   : plus bas point mort
        - breakeven_high  : plus haut point mort
        - net_cost        : coût net de la stratégie (positif = débit, négatif = crédit)

    Le ratio reward_risk sera ajouté automatiquement par StrategyEvaluator.
    """

    REQUIRED_KEYS = [
        "max_gain",
        "max_loss",
        "delta",
        "vega",
        "breakeven_low",
        "breakeven_high",
        "net_cost",
    ]

    def __init__(self, S, r, T, sigma):
        self.S = S
        self.r = r
        self.T = T
        self.sigma = sigma
        self.metrics = {}

    # ---------------------------------------------------------
    # Méthodes abstraites obligatoires
    # ---------------------------------------------------------

    @abstractmethod
    def payoff(self, S_T):
        """Payoff de la stratégie à maturité."""
        pass

    @abstractmethod
    def price(self):
        """Prix initial de la stratégie (t = 0)."""
        pass

    @abstractmethod
    def analyze(self):
        """
        Retourne un dict contenant au minimum les clés de REQUIRED_KEYS.
        Les autres métriques (theta, gamma, etc.) sont optionnelles.
        """
        pass

    @abstractmethod
    def price_at(self, S_t, T_t):
        """
        Prix de la stratégie à une date t quelconque,
        pour un sous-jacent S_t et une maturité résiduelle T_t.
        """
        pass

    # ---------------------------------------------------------
    # Méthodes utilitaires communes
    # ---------------------------------------------------------

    def compute_metrics(self):
        """
        Appelle analyze(), vérifie les clés obligatoires,
        stocke les métriques dans self.metrics et en attributs.
        """
        self.metrics = self.analyze()

        # Vérification des clés obligatoires
        for key in self.REQUIRED_KEYS:
            if key not in self.metrics:
                raise ValueError(
                    f"La stratégie {self.__class__.__name__} "
                    f"ne fournit pas la métrique obligatoire '{key}'."
                )

        # Ajout des métriques comme attributs
        for k, v in self.metrics.items():
            setattr(self, k, v)

        return self.metrics

    def summary(self):
        """Résumé textuel propre."""
        if not self.metrics:
            self.compute_metrics()

        txt = f"Résumé de la stratégie {self.__class__.__name__} :\n"
        for k, v in self.metrics.items():
            txt += f"- {k} : {v}\n"
        return txt

    def to_dict(self):
        """Retourne les métriques sous forme de dict."""
        if not self.metrics:
            self.compute_metrics()
        return self.metrics

    def plot(self, S_min=0.5, S_max=1.5, ax=None, title=None):
        """
        Trace du payoff à maturité.
        """
        S_range = np.linspace(self.S * S_min, self.S * S_max, 300)
        payoff = self.payoff(S_range)

        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 5))
        else:
            fig = ax.figure

        ax.plot(S_range, payoff, linewidth=2)
        ax.axhline(0, color="black", linewidth=1)
        ax.set_xlabel("Prix du sous-jacent à maturité")
        ax.set_ylabel("Payoff")
        ax.grid(True)

        if title:
            ax.set_title(title)

        return fig