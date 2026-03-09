from .spreads import BullCallSpread, BearPutSpread
from .straddles_strangles import Straddle, Strangle
from .butterfly import Butterfly
from .iron_condor import IronCondor


class StrategyFactory:
    """
    Factory permettant d'instancier dynamiquement une stratégie
    à partir d'un nom et d'un dictionnaire de paramètres.

    Toutes les stratégies doivent hériter de BaseStrategy.
    """

    _registry = {
        "bull_call": BullCallSpread,
        "bear_put": BearPutSpread,
        "straddle": Straddle,
        "strangle": Strangle,
        "butterfly": Butterfly,
        "iron_condor": IronCondor,
    }

    @classmethod
    def create(cls, name: str, **kwargs):
        """
        Instancie une stratégie à partir de son nom.

        Parameters
        ----------
        name : str
            Nom de la stratégie (clé du registre)
        kwargs : dict
            Paramètres nécessaires à la stratégie

        Returns
        -------
        BaseStrategy
            Instance de la stratégie correspondante
        """
        name = name.lower()

        if name not in cls._registry:
            raise ValueError(
                f"Stratégie inconnue : '{name}'. "
                f"Stratégies disponibles : {list(cls._registry.keys())}"
            )

        strategy_class = cls._registry[name]
        return strategy_class(**kwargs)

    @classmethod
    def available(cls):
        """Retourne la liste des stratégies disponibles."""
        return list(cls._registry.keys())