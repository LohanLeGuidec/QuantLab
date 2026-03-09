import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Normalisation
# ---------------------------------------------------------
def normalize(x, xmin, xmax):
    """Normalise une valeur entre 0 et 1."""
    return max(0, min(1, (x - xmin) / (xmax - xmin)))


# =========================================================
#   BEAR PUT SPREAD
# =========================================================
def score_bear_put(metrics):
    max_gain = metrics.get("max_gain", 0)
    max_loss = metrics.get("max_loss", 0)
    delta = metrics.get("delta", 0)
    cost = metrics.get("net_cost", 0)
    width = metrics.get("profit_zone_width", 0)

    gain_score = normalize(max_gain, 0, 5)
    loss_score = normalize(-max_loss, -5, 0)
    delta_score = normalize(-delta, -0.7, 0)
    cost_score = normalize(-cost, -5, 0)
    width_score = normalize(width, 0, 0.3)

    score = (
        0.30 * gain_score +
        0.25 * loss_score +
        0.20 * delta_score +
        0.15 * cost_score +
        0.10 * width_score
    )

    return int(score * 100)


# =========================================================
#   BULL CALL SPREAD
# =========================================================
def score_bull_call(metrics):
    max_gain = metrics.get("max_gain", 0)
    max_loss = metrics.get("max_loss", 0)
    delta = metrics.get("delta", 0)
    cost = metrics.get("net_cost", 0)
    width = metrics.get("profit_zone_width", 0)

    gain_score = normalize(max_gain, 0, 5)
    loss_score = normalize(-max_loss, -5, 0)
    delta_score = normalize(delta, 0, 0.7)
    cost_score = normalize(-cost, -5, 0)
    width_score = normalize(width, 0, 0.3)

    score = (
        0.30 * gain_score +
        0.25 * loss_score +
        0.20 * delta_score +
        0.15 * cost_score +
        0.10 * width_score
    )

    return int(score * 100)


# =========================================================
#   STRADDLE
# =========================================================
def score_straddle(metrics):
    vega = metrics.get("vega", 0)
    cost = metrics.get("net_cost", 0)
    max_loss = metrics.get("max_loss", 0)
    delta = metrics.get("delta", 0)
    width = metrics.get("profit_zone_width", 0)

    vega_score = normalize(vega, 0, 1)
    cost_score = normalize(-cost, -10, 0)
    loss_score = normalize(-max_loss, -10, 0)
    delta_score = normalize(-abs(delta), -0.3, 0)
    width_score = normalize(width, 0, 0.5)

    score = (
        0.40 * vega_score +
        0.20 * width_score +
        0.15 * delta_score +
        0.15 * cost_score +
        0.10 * loss_score
    )

    return int(score * 100)


# =========================================================
#   STRANGLE
# =========================================================
def score_strangle(metrics):
    vega = metrics.get("vega", 0)
    cost = metrics.get("net_cost", 0)
    max_loss = metrics.get("max_loss", 0)
    delta = metrics.get("delta", 0)
    width = metrics.get("profit_zone_width", 0)

    vega_score = normalize(vega, 0, 1)
    cost_score = normalize(-cost, -5, 0)
    loss_score = normalize(-max_loss, -5, 0)
    delta_score = normalize(-abs(delta), -0.3, 0)
    width_score = normalize(width, 0, 0.6)

    score = (
        0.35 * vega_score +
        0.25 * width_score +
        0.15 * cost_score +
        0.15 * delta_score +
        0.10 * loss_score
    )

    return int(score * 100)


# =========================================================
#   BUTTERFLY
# =========================================================
def score_butterfly(metrics):
    max_gain = metrics.get("max_gain", 0)
    max_loss = metrics.get("max_loss", 0)
    delta = metrics.get("delta", 0)
    vega = metrics.get("vega", 0)
    width = metrics.get("profit_zone_width", 0)

    gain_score = normalize(max_gain, 0, 3)
    loss_score = normalize(-max_loss, -3, 0)
    delta_score = normalize(-abs(delta), -0.2, 0)
    vega_score = normalize(-abs(vega), -0.5, 0)
    width_score = normalize(width, 0, 0.2)

    score = (
        0.25 * gain_score +
        0.25 * loss_score +
        0.20 * delta_score +
        0.20 * vega_score +
        0.10 * width_score
    )

    return int(score * 100)


# =========================================================
#   IRON CONDOR
# =========================================================
def score_iron_condor(metrics):
    max_gain = metrics.get("max_gain", 0)
    max_loss = metrics.get("max_loss", 0)
    delta = metrics.get("delta", 0)
    vega = metrics.get("vega", 0)
    width = metrics.get("profit_zone_width", 0)

    gain_score = normalize(max_gain, 0, 2)
    loss_score = normalize(-max_loss, -3, 0)
    delta_score = normalize(-abs(delta), -0.2, 0)
    vega_score = normalize(-abs(vega), -0.5, 0)
    width_score = normalize(width, 0, 0.5)

    score = (
        0.20 * gain_score +
        0.30 * loss_score +
        0.20 * delta_score +
        0.15 * vega_score +
        0.15 * width_score
    )

    return int(score * 100)


# =========================================================
#   ROUTER
# =========================================================
def score_strategy_by_name(strategy_name, metrics):
    if strategy_name == "bull_call":
        return score_bull_call(metrics)
    if strategy_name == "bear_put":
        return score_bear_put(metrics)
    if strategy_name == "straddle":
        return score_straddle(metrics)
    if strategy_name == "strangle":
        return score_strangle(metrics)
    if strategy_name == "butterfly":
        return score_butterfly(metrics)
    if strategy_name == "iron_condor":
        return score_iron_condor(metrics)
    return 50


# =========================================================
#   RADAR CHART
# =========================================================
def plot_radar(metrics, strategy_name):
    # Récupération sécurisée des valeurs
    max_gain = metrics.get("max_gain", 0)
    max_loss = -metrics.get("max_loss", 0)  # inversé : plus haut = mieux
    delta = metrics.get("delta", 0)
    vega = -abs(metrics.get("vega", 0))      # faible vega = mieux
    cost = -metrics.get("net_cost", 0)       # moins cher = mieux
    width = metrics.get("profit_zone_width", 0)

    labels = [
        "Gain potentiel",
        "Risque limité",
        "Delta",
        "Vega",
        "Coût",
        "Robustesse"
    ]

    values = [max_gain, max_loss, delta, vega, cost, width]

    # Normalisation simple
    max_abs = max(abs(v) for v in values) or 1
    values_norm = [v / max_abs for v in values]
    values_norm += values_norm[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angles, values_norm, linewidth=2, color="purple")
    ax.fill(angles, values_norm, alpha=0.25, color="purple")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    ax.set_title(f"Profil stratégique – {strategy_name}", fontsize=14, pad=20)
    ax.grid(alpha=0.3)

    return fig