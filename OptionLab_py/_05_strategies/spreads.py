import numpy as np
from .base_strategy import BaseStrategy
from .._02_Pricing.blackandscholes import black_scholes


# ============================================================
#  BULL CALL SPREAD
# ============================================================

import numpy as np
from .base_strategy import BaseStrategy
from .._02_Pricing.blackandscholes import black_scholes


# ============================================================
#  BULL CALL SPREAD
# ============================================================

class BullCallSpread(BaseStrategy):
    def __init__(self, S, r, T, sigma, K1, K2):
        super().__init__(S, r, T, sigma)
        self.K1 = K1  # strike bas
        self.K2 = K2  # strike haut

    def payoff(self, S_T):
        return np.maximum(S_T - self.K1, 0) - np.maximum(S_T - self.K2, 0)

    def price(self):
        c1 = black_scholes(self.S, self.K1, self.r, self.T, self.sigma, "call")
        c2 = black_scholes(self.S, self.K2, self.r, self.T, self.sigma, "call")
        return c1 - c2  # coût positif (débit)

    def price_at(self, S_t, T_t):
        c1 = black_scholes(S_t, self.K1, self.r, T_t, self.sigma, "call")
        c2 = black_scholes(S_t, self.K2, self.r, T_t, self.sigma, "call")
        return c1 - c2

    def analyze(self):
        metrics = {}

        # Coût net (débit)
        cost = self.price()
        metrics["cost"] = cost
        metrics["net_cost"] = cost

        # Largeur du spread
        width = self.K2 - self.K1

        # Max gain / max loss
        metrics["max_gain"] = width - cost
        metrics["max_loss"] = cost

        # Breakeven
        metrics["breakeven_low"] = self.K1 + cost
        metrics["breakeven_high"] = self.K2

        # Delta numérique
        h = 0.01 * self.S
        price_up = self.price_at(self.S + h, self.T)
        price_down = self.price_at(self.S - h, self.T)
        metrics["delta"] = (price_up - price_down) / (2 * h)

        # Vega numérique
        sigma_up = self.sigma + 0.01
        sigma_down = self.sigma - 0.01

        price_sigma_up = (
            black_scholes(self.S, self.K1, self.r, self.T, sigma_up, "call")
            - black_scholes(self.S, self.K2, self.r, self.T, sigma_up, "call")
        )
        price_sigma_down = (
            black_scholes(self.S, self.K1, self.r, self.T, sigma_down, "call")
            - black_scholes(self.S, self.K2, self.r, self.T, sigma_down, "call")
        )

        metrics["vega"] = (price_sigma_up - price_sigma_down) / 0.02

        # Largeur relative
        metrics["profit_zone_width"] = width / self.S

        return metrics

    def plot(self, S_min=0.5, S_max=1.5, ax=None):
        return super().plot(S_min, S_max, ax, "Bull Call Spread – Payoff")


# ============================================================
#  BEAR PUT SPREAD
# ============================================================

class BearPutSpread(BaseStrategy):
    def __init__(self, S, r, T, sigma, K1, K2):
        super().__init__(S, r, T, sigma)
        self.K1 = K1  # strike bas
        self.K2 = K2  # strike haut

    def payoff(self, S_T):
        # Achat put K2 (haut), vente put K1 (bas)
        return np.maximum(self.K2 - S_T, 0) - np.maximum(self.K1 - S_T, 0)

    def price(self):
        p1 = black_scholes(self.S, self.K1, self.r, self.T, self.sigma, "put")
        p2 = black_scholes(self.S, self.K2, self.r, self.T, self.sigma, "put")
        return p2 - p1  # coût positif (débit) car p2 > p1

    def price_at(self, S_t, T_t):
        p1 = black_scholes(S_t, self.K1, self.r, T_t, self.sigma, "put")
        p2 = black_scholes(S_t, self.K2, self.r, T_t, self.sigma, "put")
        return p2 - p1

    def analyze(self):
        metrics = {}

        # Coût net (débit)
        cost = self.price()
        metrics["cost"] = cost
        metrics["net_cost"] = cost

        # Largeur du spread
        width = self.K2 - self.K1  # toujours positif car K2 > K1

        # Max gain / max loss
        metrics["max_gain"] = width - cost
        metrics["max_loss"] = cost

        # Breakeven
        metrics["breakeven_low"] = self.K2 - cost
        metrics["breakeven_high"] = self.K1

        # Delta numérique
        h = 0.001 * self.S
        price_up = self.price_at(self.S + h, self.T)
        price_down = self.price_at(self.S - h, self.T)
        metrics["delta"] = (price_up - price_down) / (2 * h)

        # Vega numérique
        sigma_up = self.sigma + 0.01
        sigma_down = self.sigma - 0.01

        price_sigma_up = (
            black_scholes(self.S, self.K2, self.r, self.T, sigma_up, "put")
            - black_scholes(self.S, self.K1, self.r, self.T, sigma_up, "put")
        )
        price_sigma_down = (
            black_scholes(self.S, self.K2, self.r, self.T, sigma_down, "put")
            - black_scholes(self.S, self.K1, self.r, self.T, sigma_down, "put")
        )

        metrics["vega"] = (price_sigma_up - price_sigma_down) / 0.02

        # Largeur relative
        metrics["profit_zone_width"] = width / self.S

        return metrics

    def plot(self, S_min=0.5, S_max=1.5, ax=None):
        return super().plot(S_min, S_max, ax, "Bear Put Spread – Payoff")