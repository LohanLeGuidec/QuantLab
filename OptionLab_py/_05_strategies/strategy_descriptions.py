def smart_summary(strategy_name: str) -> str:
    """
    Retourne un résumé pédagogique et cohérent pour chaque stratégie.
    """

    summaries = {
        "bull_call": (
            "Stratégie haussière à risque limité. "
            "Gain plafonné si le sous-jacent dépasse le strike supérieur. "
            "Idéale pour jouer une hausse modérée avec un budget maîtrisé."
        ),

        "bear_put": (
            "Stratégie baissière à risque limité. "
            "Gain plafonné si le sous-jacent passe sous le strike inférieur. "
            "Idéale pour jouer une baisse modérée avec un coût maîtrisé."
        ),

        "straddle": (
            "Stratégie neutre directionnellement mais très sensible à la volatilité. "
            "Vous gagnez si le sous-jacent bouge fortement dans un sens ou dans l’autre."
        ),

        "strangle": (
            "Stratégie long volatilité moins coûteuse qu’un straddle. "
            "Vous gagnez si le sous-jacent sort d’un large corridor."
        ),

        "butterfly": (
            "Stratégie short volatilité à risque limité. "
            "Vous gagnez si le sous-jacent termine proche du strike central."
        ),

        "iron_condor": (
            "Stratégie short volatilité avec risque et gain limités. "
            "Vous gagnez si le sous-jacent reste dans un corridor défini."
        ),
    }

    return summaries.get(strategy_name, "Résumé non disponible.")