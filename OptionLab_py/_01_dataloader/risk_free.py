import pandas_datareader.data as web

def risk_free_rate(region):
    if region == "US":
        r = web.DataReader("DGS3MO", "fred").iloc[-1].values[0] / 100          # US 3M T-Bill
    elif region == "EU":
        r = web.DataReader("IR3TIB01EZM156N", "fred").iloc[-1].values[0] / 100 # Eurozone 3M interbank
    elif region == "JP":
        r = web.DataReader("IR3TIB01JPM156N", "fred").iloc[-1].values[0] / 100 # Japan 3M interbank
    elif region == "CA":
        r = web.DataReader("IR3TIB01CAM156N", "fred").iloc[-1].values[0] / 100 # Canada 3M interbank
    elif region == "AU":
        r = web.DataReader("IR3TIB01AUM156N", "fred").iloc[-1].values[0] / 100 # Australia 3M interbank
    elif region == "IN":
        r = web.DataReader("IR3TIB01INM156N", "fred").iloc[-1].values[0] / 100 # India 3M interbank
    elif region == "CN":
        r = web.DataReader("IR3TIB01CNM156N", "fred").iloc[-1].values[0] / 100 # China 3M interbank
    else:
        r = 0.03  # fallback

    print(f"Taux sans risque estimé pour la région {region} : {r:.4f}")
    return r
