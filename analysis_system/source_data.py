import yfinance as yf
import sys
import os

def fetch_data_yahoo(ticker, period):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def save_to_csv(data, ticker, market, period):
    filename = f"data_{ticker}_{market}_{period}.csv"
    data.to_csv(f"analysis_system/data/{filename}")
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: source_data.py <SYMBOL> <MARKET> <PERIOD>")
        sys.exit(1)

    symbol = sys.argv[1]
    market = sys.argv[2]
    period = sys.argv[3]

    # Map to the correct Yahoo Finance ticker symbol based on market
    ticker_map = {
        "US": symbol,
        "UK": symbol + ".L",   # UK symbols typically end with .L on Yahoo Finance
        "AU": symbol + ".AX",  # Australian symbols typically end with .AX on Yahoo Finance
        "HK": symbol + ".HK",  # Hong Kong symbols typically end with .HK on Yahoo Finance
        "CN": symbol + ".SS" if "600" <= symbol <= "604" else symbol + ".SZ"  # Shanghai and Shenzhen, respectively
    }
    
    ticker = ticker_map.get(market)
    if not ticker:
        print(f"Market '{market}' is not supported or the ticker mapping is missing.")
        sys.exit(1)

    data = fetch_data_yahoo(ticker, period)
    save_to_csv(data, symbol, market, period)
