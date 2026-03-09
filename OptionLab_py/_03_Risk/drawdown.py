def compute_drawdown(series):
    """
    Calcule le drawdown et le max drawdown.
    """
    cumulative = series / series.iloc[0]
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_dd = drawdown.min()
    return drawdown, max_dd

def drawdown_(series):
    """
    Retourne uniquement la série de drawdown.
    """
    cumulative = series / series.iloc[0]
    peak = cumulative.cummax()
    return (cumulative - peak) / peak