import os
import sys

# Update the imports based on the directory structure
from analysis_system.source_data import fetch_data_yahoo, save_to_csv
from analysis_system.cleaning import load_data, clean_data, save_cleaned_data
from analysis_system.visualize import visualize_data
from analysis_system.stat import descriptive_statistics, growth_rate, volatility, max_drawdown_percent

def main():
    # Check user inputs
    if len(sys.argv) != 4:
        print("Usage: main.py <SYMBOL> <MARKET> <PERIOD>")
        sys.exit(1)

    symbol = sys.argv[1]
    market = sys.argv[2]
    period = sys.argv[3]

    # Paths are adjusted for the directory structure
    raw_data_filename = os.path.join("analysis_system", "data", f"data_{symbol}_{market}_{period}.csv")

    data = fetch_data_yahoo(symbol, period)
    save_to_csv(data, symbol, market, period)

    # Clean Data
    cleaned_data_filename = os.path.join("analysis_system", "data", f"cleaned_{symbol}_{market}_{period}.csv")
    data = load_data(raw_data_filename)
    cleaned_data = clean_data(data)
    save_cleaned_data(cleaned_data, cleaned_data_filename)

    # Display Statistics
    print("\nDescriptive Statistics:")
    print(descriptive_statistics(cleaned_data))
    print("\nGrowth Rate (%):", growth_rate(cleaned_data))
    print("Volatility (%):", volatility(cleaned_data))
    print("Max Drawdown (%):", max_drawdown_percent(cleaned_data))
    print("---------------------------------------------------------------")

    # Visualize Data
    visualize_data(cleaned_data_filename)

if __name__ == "__main__":
    main()
# Run the program with the following command:
# py main.py AAPL US 1y