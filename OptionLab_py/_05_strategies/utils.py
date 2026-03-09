import numpy as np

def auto_offset(S: float, sigma: float, T: float) -> float:
    """
    Calcule automatiquement un offset pertinent pour les strikes
    en fonction de la volatilité historique et de l'échéance.

    L’offset correspond à :
        S * sigma * sqrt(T)
    avec un minimum de 2 pour éviter des spreads trop serrés.

    Parameters
    ----------
    S : float
        Spot du sous-jacent
    sigma : float
        Volatilité historique annualisée
    T : float
        Maturité en années

    Returns
    -------
    float
        Offset arrondi, toujours >= 2
    """
    return max(2, round(S * sigma * np.sqrt(T)))