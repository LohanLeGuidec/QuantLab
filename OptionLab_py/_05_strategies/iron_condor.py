import numpy as np
from .base_strategy import BaseStrategy
from .._02_Pricing.blackandscholes import black_scholes


class IronCondor(BaseStrategy):
    """
    Short Iron Condor :
    +1 put K1
    -1 put K2
    -1 call K3
    +1 call K4
    avec K1 < K2 < K3 < K4
    """

    def __init__(self, S, r, T, sigma, K1, K2, K3, K4):
        super().__init__(S, r, T, sigma)
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.K4 = K4

    # ---------------------------------------------------------
    # Payoff
    # ---------------------------------------------------------
    def payoff(self, S_T):
        put_long = np.maximum(self.K1 - S_T, 0)
        put_short = -np.maximum(self.K2 - S_T, 0)
        call_short = -np.maximum(S_T - self.K3, 0)
        call_long = np.maximum(S_T - self.K4, 0)
        return put_long + put_short + call_short + call_long

    # ---------------------------------------------------------
    # Pricing
    # ---------------------------------------------------------
    def price(self):
        p1 = black_scholes(self.S, self.K1, self.r, self.T, self.sigma, "put")
        p2 = black_scholes(self.S, self.K2, self.r, self.T, self.sigma, "put")
        c3 = black_scholes(self.S, self.K3, self.r, self.T, self.sigma, "call")
        c4 = black_scholes(self.S, self.K4, self.r, self.T, self.sigma, "call")
        return p1 - p2 - c3 + c4  # crédit reçu

    def price_at(self, S_t, T_t):
        p1 = black_scholes(S_t, self.K1, self.r, T_t, self.sigma, "put")
        p2 = black_scholes(S_t, self.K2, self.r, T_t, self.sigma, "put")
        c3 = black_scholes(S_t, self.K3, self.r, T_t, self.sigma, "call")
        c4 = black_scholes(S_t, self.K4, self.r, T_t, self.sigma, "call")
        return p1 - p2 - c3 + c4

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
            - credit
            - profit_zone_width
        """
        metrics = {}

        # Crédit reçu (positif)
        credit = self.price()
        metrics["credit"] = credit

        # Coût net (négatif car stratégie short)
        metrics["net_cost"] = -credit
        metrics["cost"] = -credit

        # Largeur des ailes (symétrique)
        wing_width = self.K2 - self.K1

        # Max gain = crédit
        metrics["max_gain"] = credit

        # Max loss = largeur - crédit
        metrics["max_loss"] = wing_width - credit

        # Breakeven
        metrics["breakeven_low"] = self.K2 - credit
        metrics["breakeven_high"] = self.K3 + credit

        # Delta numérique
        h = 0.01 * self.S
        price_up = self.price_at(self.S + h, self.T)
        price_down = self.price_at(self.S - h, self.T)
        metrics["delta"] = (price_up - price_down) / (2 * h)

        # Vega numérique
        sigma_up = self.sigma + 0.01
        sigma_down = self.sigma - 0.01

        price_sigma_up = (
            black_scholes(self.S, self.K1, self.r, self.T, sigma_up, "put")
            - black_scholes(self.S, self.K2, self.r, self.T, sigma_up, "put")
            - black_scholes(self.S, self.K3, self.r, self.T, sigma_up, "call")
            + black_scholes(self.S, self.K4, self.r, self.T, sigma_up, "call")
        )

        price_sigma_down = (
            black_scholes(self.S, self.K1, self.r, self.T, sigma_down, "put")
            - black_scholes(self.S, self.K2, self.r, self.T, sigma_down, "put")
            - black_scholes(self.S, self.K3, self.r, self.T, sigma_down, "call")
            + black_scholes(self.S, self.K4, self.r, self.T, sigma_down, "call")
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
        return super().plot(
            S_min=S_min,
            S_max=S_max,
            ax=ax,
            title="Short Iron Condor – Payoff",
        )