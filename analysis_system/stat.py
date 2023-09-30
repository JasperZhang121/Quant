import pandas as pd
import sys
from empyrical import (max_drawdown, annual_return, annual_volatility, 
                       sharpe_ratio, sortino_ratio, omega_ratio, 
                       calmar_ratio, tail_ratio, cum_returns_final)

def load_data(filename):
    """Load the CSV data into a DataFrame."""
    return pd.read_csv(filename, parse_dates=['Date'], index_col='Date')

def daily_returns(data):
    """Compute daily returns for the Close column."""
    return data['Close'].pct_change().dropna()

def descriptive_statistics(data):
    """Return basic statistics for the Close column."""
    return data['Close'].describe()

def growth_rate(data):
    """Calculate the growth rate."""
    returns = daily_returns(data)
    return annual_return(returns) * 100

def volatility(data):
    """Calculate the stock's volatility."""
    returns = daily_returns(data)
    return annual_volatility(returns) * 100

def max_drawdown_percent(data):
    """Calculate the maximum drawdown."""
    returns = daily_returns(data)
    return max_drawdown(returns) * 100

def get_sharpe_ratio(data):
    """Calculate the Sharpe ratio."""
    returns = daily_returns(data)
    return sharpe_ratio(returns)

def get_sortino_ratio(data):
    """Calculate the Sortino ratio."""
    returns = daily_returns(data)
    return sortino_ratio(returns)

def get_omega_ratio(data):
    """Calculate the Omega ratio."""
    returns = daily_returns(data)
    return omega_ratio(returns)

def get_calmar_ratio(data):
    """Calculate the Calmar ratio."""
    returns = daily_returns(data)
    return calmar_ratio(returns)

def get_tail_ratio(data):
    """Calculate the tail ratio."""
    returns = daily_returns(data)
    return tail_ratio(returns)

def get_cumulative_returns(data):
    """Calculate the cumulative returns."""
    returns = daily_returns(data)
    return cum_returns_final(returns) * 100

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: stat.py <FILENAME>")
        sys.exit(1)

    filename = sys.argv[1]
    data = load_data(filename)
    
    print("\nDescriptive Statistics:")
    print(descriptive_statistics(data))
    print("\nGrowth Rate (%):", growth_rate(data))
    print("Volatility (%):", volatility(data))
    print("Max Drawdown (%):", max_drawdown_percent(data))
    print("Sharpe Ratio:", get_sharpe_ratio(data))
    print("Sortino Ratio:", get_sortino_ratio(data))
    print("Omega Ratio:", get_omega_ratio(data))
    print("Calmar Ratio:", get_calmar_ratio(data))
    print("Tail Ratio:", get_tail_ratio(data))
    print("Cumulative Returns (%):", get_cumulative_returns(data))
    print("---------------------------------------------------------------")