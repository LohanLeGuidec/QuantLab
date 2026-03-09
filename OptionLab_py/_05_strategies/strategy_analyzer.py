import pandas as pd
from .spreads import BullCallSpread, BearPutSpread
from .straddles_strangles import Straddle, Strangle
from .butterfly import Butterfly
from .iron_condor import IronCondor


def run_strategy_analyzer(S, K, r, T, sigma):
    """
    Compare plusieurs stratégies optionnelles :
    - Bull Call Spread
    - Bear Put Spread
    - Straddle
    - Strangle
    - Butterfly
    - Iron Condor
    """

    results = []

    # 1) Bull Call Spread
    spread = BullCallSpread(S, r, T, sigma, K1=K, K2=K + 10).compute_metrics()
    results.append({
        "Strategy": "Bull Call Spread",
        "Cost / Credit": spread["net_cost"],
        "Max Gain": spread["max_gain"],
        "Max Loss": spread["max_loss"],
        "BE Low": spread["breakeven_low"],
        "BE High": spread["breakeven_high"],
        "Type": "Directionnelle (haussière)"
    })

    # 2) Bear Put Spread
    bear = BearPutSpread(S, r, T, sigma, K1=K, K2=K - 10).compute_metrics()
    results.append({
        "Strategy": "Bear Put Spread",
        "Cost / Credit": bear["net_cost"],
        "Max Gain": bear["max_gain"],
        "Max Loss": bear["max_loss"],
        "BE Low": bear["breakeven_low"],
        "BE High": bear["breakeven_high"],
        "Type": "Directionnelle (baissière)"
    })

    # 3) Straddle
    straddle = Straddle(S, r, T, sigma, K).compute_metrics()
    results.append({
        "Strategy": "Straddle",
        "Cost / Credit": straddle["net_cost"],
        "Max Gain": straddle["max_gain"],
        "Max Loss": straddle["max_loss"],
        "BE Low": straddle["breakeven_low"],
        "BE High": straddle["breakeven_high"],
        "Type": "Long Vol"
    })

    # 4) Strangle
    strangle = Strangle(S, r, T, sigma, K1=K - 10, K2=K + 10).compute_metrics()
    results.append({
        "Strategy": "Strangle",
        "Cost / Credit": strangle["net_cost"],
        "Max Gain": strangle["max_gain"],
        "Max Loss": strangle["max_loss"],
        "BE Low": strangle["breakeven_low"],
        "BE High": strangle["breakeven_high"],
        "Type": "Long Vol"
    })

    # 5) Butterfly
    bfly = Butterfly(S, r, T, sigma, K1=K - 10, K2=K, K3=K + 10).compute_metrics()
    results.append({
        "Strategy": "Butterfly",
        "Cost / Credit": bfly["net_cost"],
        "Max Gain": bfly["max_gain"],
        "Max Loss": bfly["max_loss"],
        "BE Low": bfly["breakeven_low"],
        "BE High": bfly["breakeven_high"],
        "Type": "Short Vol"
    })

    # 6) Iron Condor
    ic = IronCondor(S, r, T, sigma, K1=K - 20, K2=K - 10, K3=K + 10, K4=K + 20).compute_metrics()
    results.append({
        "Strategy": "Iron Condor",
        "Cost / Credit": ic["net_cost"],  # harmonisé
        "Max Gain": ic["max_gain"],
        "Max Loss": ic["max_loss"],
        "BE Low": ic["breakeven_low"],
        "BE High": ic["breakeven_high"],
        "Type": "Short Vol"
    })

    return pd.DataFrame(results)