import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .strategy_factory import StrategyFactory


# ============================================================
#  STRATEGY EVALUATOR
# ============================================================

class StrategyEvaluator:
    """
    Évalue une stratégie OO en utilisant ses méthodes internes.
    """

    @staticmethod
    def evaluate(strategy):
        # compute_metrics() = version complète et harmonisée
        analysis = strategy.compute_metrics()

        # Conversion propre des np.float64 → float
        clean = {}
        for k, v in analysis.items():
            if hasattr(v, "item"):
                clean[k] = float(v)
            else:
                clean[k] = v

        # Ajout du ratio reward/risk si possible
        if (
            "max_gain" in clean
            and "max_loss" in clean
            and clean["max_loss"] not in (0, None)
        ):
            clean["reward_risk"] = clean["max_gain"] / clean["max_loss"]

        return clean


# ============================================================
#  STRATEGY OPTIMIZER
# ============================================================

class StrategyOptimizer:
    """
    Optimiseur basé sur une recherche par grille + outils d'analyse agrégée.
    """

    def __init__(self, S, r, T, sigma):
        self.S = S
        self.r = r
        self.T = T
        self.sigma = sigma

    # --------------------------------------------------------
    #  OPTIMISATION D’UNE STRATÉGIE
    # --------------------------------------------------------
    def optimize(self, strategy_name, param_grid, objective="reward_risk"):
        """
        Teste plusieurs stratégies et retourne la meilleure selon un critère.

        param_grid : liste de dictionnaires contenant les paramètres à tester
        objective  : clé du dictionnaire d'analyse (ex: 'max_gain', 'reward_risk')
        """

        best_strategy = None
        best_score = -np.inf
        best_params = None

        for params in param_grid:
            # Création de la stratégie via la factory
            strategy = StrategyFactory.create(
                strategy_name,
                S=self.S, r=self.r, T=self.T, sigma=self.sigma,
                **params
            )

            # Évaluation complète
            results = StrategyEvaluator.evaluate(strategy)

            if objective not in results:
                continue

            score = results[objective]

            if score > best_score:
                best_score = score
                best_strategy = strategy
                best_params = params

        return best_strategy, best_score, best_params

    # --------------------------------------------------------
    #  OPTIMISATION DE TOUTES LES STRATÉGIES
    # --------------------------------------------------------
    def run_all(self, optimizations, objective="reward_risk"):
        """
        Lance l'optimisation pour toutes les stratégies définies dans 'optimizations'.

        Retourne :
            - df : DataFrame récapitulatif
            - best_strategies : dict {name: {"strategy", "score", "params", "analysis"}}
        """
        results = []
        best_strategies = {}

        for strategy_name, config in optimizations.items():
            best_strategy, best_score, best_params = self.optimize(
                strategy_name,
                config["param_grid"],
                objective=objective
            )

            analysis = StrategyEvaluator.evaluate(best_strategy)

            row = {
                "Strategy": strategy_name,
                "Title": config.get("title", strategy_name),
                "Score": best_score,
            }

            # Ajout des métriques disponibles
            for k, v in analysis.items():
                row[k] = v

            results.append(row)

            best_strategies[strategy_name] = {
                "strategy": best_strategy,
                "score": best_score,
                "params": best_params,
                "analysis": analysis,
                "title": config.get("title", strategy_name),
            }

        df = pd.DataFrame(results)
        return df, best_strategies

    # --------------------------------------------------------
    #  CLASSEMENT
    # --------------------------------------------------------
    @staticmethod
    def rank(df, by="Score", ascending=False):
        """Classement des stratégies selon une colonne."""
        if by not in df.columns:
            return df
        return df.sort_values(by=by, ascending=ascending)

    # --------------------------------------------------------
    #  RADAR CHART
    # --------------------------------------------------------
    @staticmethod
    def radar_chart(df, metrics=None):
        """
        Construit un radar chart à partir d'un DataFrame de résultats.
        """

        if metrics is None:
            metrics = ["max_gain", "max_loss", "reward_risk", "vega"]

        available_metrics = [m for m in metrics if m in df.columns]
        if not available_metrics:
            raise ValueError("Aucune des métriques demandées n'est présente dans le DataFrame.")

        work_df = df.copy()
        work_df[available_metrics] = work_df[available_metrics].fillna(0)

        # Normalisation 0–1
        norm_df = work_df.copy()
        for col in available_metrics:
            col_min = norm_df[col].min()
            col_max = norm_df[col].max()
            if col_max - col_min == 0:
                norm_df[col] = 0.5
            else:
                norm_df[col] = (norm_df[col] - col_min) / (col_max - col_min)

        angles = np.linspace(0, 2 * np.pi, len(available_metrics), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        for _, row in norm_df.iterrows():
            values = row[available_metrics].tolist()
            values += values[:1]
            ax.plot(angles, values, linewidth=2, label=row["Strategy"])
            ax.fill(angles, values, alpha=0.15)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(available_metrics)
        ax.set_title("Radar Chart – Profil de risque")
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

        return fig