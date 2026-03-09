import yfinance as yf

def get_region_from_currency(currency):
    currency_region_map = {
            "USD": "US",
            "EUR": "EU",
            "GBP": "UK",
            "JPY": "JP",
            "CAD": "CA",
            "AUD": "AU",
            "INR": "IN",
            "CNY": "CN",
            
        }
    return currency_region_map.get(currency, "US")  

def get_region_from_ticker(ticker):
    data = yf.Ticker(ticker)
    currency = data.info.get("currency", "USD")
    return get_region_from_currency(currency)