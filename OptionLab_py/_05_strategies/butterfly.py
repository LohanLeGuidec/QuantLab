import numpy as np
from .base_strategy import BaseStrategy
from .._02_Pricing.blackandscholes import black_scholes


class Butterfly(BaseStrategy):
    """
    Butterfly (call ou put) :
    +1 option K1
    -2 options K2
    +1 option K3
    """

    def __init__(self, S, r, T, sigma, K1, K2, K3, option_type="call"):
        super().__init__(S, r, T, sigma)
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.option_type = option_type.lower()

    # ---------------------------------------------------------
    # Payoff
    # ---------------------------------------------------------
    def payoff(self, S_T):
        if self.option_type == "call":
            return (
                np.maximum(S_T - self.K1, 0)
                - 2 * np.maximum(S_T - self.K2, 0)
                + np.maximum(S_T - self.K3, 0)
            )
        else:
            return (
                np.maximum(self.K1 - S_T, 0)
                - 2 * np.maximum(self.K2 - S_T, 0)
                + np.maximum(self.K3 - S_T, 0)
            )

    # ---------------------------------------------------------
    # Pricing
    # ---------------------------------------------------------
    def price(self):
        def bs(K):
            return black_scholes(self.S, K, self.r, self.T, self.sigma, self.option_type)

        return bs(self.K1) - 2 * bs(self.K2) + bs(self.K3)

    def price_at(self, S_t, T_t):
        def bs(K):
            return black_scholes(S_t, K, self.r, T_t, self.sigma, self.option_type)

        return bs(self.K1) - 2 * bs(self.K2) + bs(self.K3)

    # ---------------------------------------------------------
    # Analyse 
    # ---------------------------------------------------------
    def analyze(self):
        """
        Retourne un dict harmonisé avec BaseStrategy.REQUIRED_KEYS :
            - max_gain
            - max_loss
            - delta
            - vega
            - breakeven_low
            - breakeven_high
            - net_cost
        + métriques supplémentaires :
            - cost
            - profit_zone_width
        """
        metrics = {}

        # Coût net (débit > 0)
        cost = self.price()
        metrics["cost"] = cost
        metrics["net_cost"] = cost

        # Largeur du butterfly
        width = self.K2 - self.K1

        # Max gain / max loss
        metrics["max_gain"] = width - cost
        metrics["max_loss"] = cost

        # Breakeven
        metrics["breakeven_low"] = self.K1 + cost
        metrics["breakeven_high"] = self.K3 - cost

        # Delta numérique
        h = 0.01 * self.S
        price_up = self.price_at(self.S + h, self.T)
        price_down = self.price_at(self.S - h, self.T)
        metrics["delta"] = (price_up - price_down) / (2 * h)

        # Vega numérique (autour du strike central)
        sigma_up = self.sigma + 0.01
        sigma_down = self.sigma - 0.01

        price_sigma_up = black_scholes(
            self.S, self.K2, self.r, self.T, sigma_up, self.option_type
        )
        price_sigma_down = black_scholes(
            self.S, self.K2, self.r, self.T, sigma_down, self.option_type
        )

        metrics["vega"] = (price_sigma_up - price_sigma_down) / 0.02

        # Largeur relative de la zone profitable
        metrics["profit_zone_width"] = (
            metrics["breakeven_high"] - metrics["breakeven_low"]
        ) / self.S

        return metrics

    # ---------------------------------------------------------
    # Plot
    # ---------------------------------------------------------
    def plot(self, S_min=0.5, S_max=1.5, ax=None):
        title = f"Butterfly {self.option_type.capitalize()} – Payoff"
        return super().plot(S_min=S_min, S_max=S_max, ax=ax, title=title)