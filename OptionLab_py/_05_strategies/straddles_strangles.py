import numpy as np
from .base_strategy import BaseStrategy
from .._02_Pricing.blackandscholes import black_scholes


# ============================================================
#  STRADDLE
# ============================================================

class Straddle(BaseStrategy):
    """
    Straddle :
    - Achat call K
    - Achat put K
    """

    def __init__(self, S, r, T, sigma, K):
        super().__init__(S, r, T, sigma)
        self.K = K

    def payoff(self, S_T):
        return np.maximum(S_T - self.K, 0) + np.maximum(self.K - S_T, 0)

    def price(self):
        call = black_scholes(self.S, self.K, self.r, self.T, self.sigma, "call")
        put = black_scholes(self.S, self.K, self.r, self.T, self.sigma, "put")
        return call + put  # coût positif (débit)

    def price_at(self, S_t, T_t):
        call = black_scholes(S_t, self.K, self.r, T_t, self.sigma, "call")
        put = black_scholes(S_t, self.K, self.r, T_t, self.sigma, "put")
        return call + put

    def analyze(self):
        metrics = {}

        # Coût net (débit)
        cost = self.price()
        metrics["cost"] = cost
        metrics["net_cost"] = cost

        # Max loss = coût
        metrics["max_loss"] = cost

        # Max gain = inf (mais on met un proxy réaliste)
        S_up = self.S * np.exp(3 * self.sigma * np.sqrt(self.T))
        metrics["max_gain"] = abs(S_up - self.K) - cost

        # Breakeven
        metrics["breakeven_low"] = self.K - cost
        metrics["breakeven_high"] = self.K + cost

        # Delta numérique
        h = 0.01 * self.S
        price_up = self.price_at(self.S + h, self.T)
        price_down = self.price_at(self.S - h, self.T)
        metrics["delta"] = (price_up - price_down) / (2 * h)

        # Vega numérique
        sigma_up = self.sigma + 0.01
        sigma_down = self.sigma - 0.01

        price_sigma_up = (
            black_scholes(self.S, self.K, self.r, self.T, sigma_up, "call")
            + black_scholes(self.S, self.K, self.r, self.T, sigma_up, "put")
        )
        price_sigma_down = (
            black_scholes(self.S, self.K, self.r, self.T, sigma_down, "call")
            + black_scholes(self.S, self.K, self.r, self.T, sigma_down, "put")
        )

        metrics["vega"] = (price_sigma_up - price_sigma_down) / 0.02

        # Largeur relative de la zone profitable
        metrics["profit_zone_width"] = (
            metrics["breakeven_high"] - metrics["breakeven_low"]
        ) / self.S

        return metrics

    def plot(self, S_min=0.5, S_max=1.5, ax=None):
        return super().plot(
            S_min=S_min, S_max=S_max, ax=ax, title="Straddle – Payoff"
        )


# ============================================================
#  STRANGLE
# ============================================================

class Strangle(BaseStrategy):
    """
    Strangle :
    - Achat put K1
    - Achat call K2
    """

    def __init__(self, S, r, T, sigma, K1, K2):
        super().__init__(S, r, T, sigma)
        self.K1 = K1
        self.K2 = K2

    def payoff(self, S_T):
        return np.maximum(self.K1 - S_T, 0) + np.maximum(S_T - self.K2, 0)

    def price(self):
        put = black_scholes(self.S, self.K1, self.r, self.T, self.sigma, "put")
        call = black_scholes(self.S, self.K2, self.r, self.T, self.sigma, "call")
        return put + call  # coût positif (débit)

    def price_at(self, S_t, T_t):
        put = black_scholes(S_t, self.K1, self.r, T_t, self.sigma, "put")
        call = black_scholes(S_t, self.K2, self.r, T_t, self.sigma, "call")
        return put + call

    def analyze(self):
        metrics = {}

        # Coût net (débit)
        cost = self.price()
        metrics["cost"] = cost
        metrics["net_cost"] = cost

        # Max loss = coût
        metrics["max_loss"] = cost

        # Max gain proxy (mouvement extrême)
        S_up = self.S * np.exp(3 * self.sigma * np.sqrt(self.T))
        gain_up = max(self.K1 - S_up, 0) + max(S_up - self.K2, 0) - cost
        metrics["max_gain"] = gain_up

        # Breakeven
        metrics["breakeven_low"] = self.K1 - cost
        metrics["breakeven_high"] = self.K2 + cost

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
            + black_scholes(self.S, self.K2, self.r, self.T, sigma_up, "call")
        )
        price_sigma_down = (
            black_scholes(self.S, self.K1, self.r, self.T, sigma_down, "put")
            + black_scholes(self.S, self.K2, self.r, self.T, sigma_down, "call")
        )

        metrics["vega"] = (price_sigma_up - price_sigma_down) / 0.02

        # Largeur relative
        metrics["profit_zone_width"] = (
            metrics["breakeven_high"] - metrics["breakeven_low"]
        ) / self.S

        return metrics

    def plot(self, S_min=0.5, S_max=1.5, ax=None):
        return super().plot(
            S_min=S_min, S_max=S_max, ax=ax, title="Strangle – Payoff"
        )