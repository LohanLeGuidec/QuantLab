"""
Grilles d’optimisation standardisées pour StrategyOptimizer.

Chaque entrée contient :
    - title : nom lisible de la stratégie optimisée
    - param_grid : liste de dictionnaires de paramètres à tester

Les clés correspondent exactement aux paramètres attendus par StrategyFactory.
"""

def build_optimization_grid(K: float, offset: float):
    return {
        "bull_call": {
            "title": "Optimized Bull Call Spread",
            "param_grid": [
                {"K1": K - 2 * offset, "K2": K - offset},
                {"K1": K - offset, "K2": K},
                {"K1": K, "K2": K + offset},
                {"K1": K + offset, "K2": K + 2 * offset},
            ],
        },

        "bear_put": {
            "title": "Optimized Bear Put Spread",
            "param_grid": [
                {"K1": K + 2 * offset, "K2": K + offset},
                {"K1": K + offset, "K2": K},
                {"K1": K, "K2": K - offset},
                {"K1": K - offset, "K2": K - 2 * offset},
            ],
        },

        "straddle": {
            "title": "Optimized Straddle",
            "param_grid": [
                {"K": K - 2 * offset},
                {"K": K - offset},
                {"K": K},
                {"K": K + offset},
                {"K": K + 2 * offset},
            ],
        },

        "strangle": {
            "title": "Optimized Strangle",
            "param_grid": [
                {"K1": K - offset, "K2": K + offset},
                {"K1": K - 2 * offset, "K2": K + 2 * offset},
                {"K1": K - 3 * offset, "K2": K + 3 * offset},
            ],
        },

        "butterfly": {
            "title": "Optimized Butterfly",
            "param_grid": [
                {"K1": K - 2 * offset, "K2": K, "K3": K + 2 * offset, "option_type": "call"},
                {"K1": K - offset, "K2": K, "K3": K + offset, "option_type": "call"},
            ],
        },

        "iron_condor": {
            "title": "Optimized Iron Condor",
            "param_grid": [
                {"K1": K - 3 * offset, "K2": K - offset, "K3": K + offset, "K4": K + 3 * offset},
                {"K1": K - 2 * offset, "K2": K - offset, "K3": K + offset, "K4": K + 2 * offset},
            ],
        },
    }