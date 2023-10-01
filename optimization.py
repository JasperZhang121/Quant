import pandas as pd
import numpy as np
import argparse
from scipy.optimize import minimize

def portfolio_annualized_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return std, returns

def objective(weights, mean_returns, cov_matrix, target_return):
    portfolio_std, portfolio_return = portfolio_annualized_performance(weights, mean_returns, cov_matrix)
    return np.abs(portfolio_return - target_return)

def optimize_portfolio(filepath):
    data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
    returns = data.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple((0,1) for asset in range(num_assets))
    
    target_returns = np.linspace(min(mean_returns), max(mean_returns), 50)
    efficient_portfolios = []
    
    for target in target_returns:
        args = (mean_returns, cov_matrix, target)
        result = minimize(objective, num_assets*[1./num_assets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
        efficient_portfolios.append(result)

    return efficient_portfolios

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Portfolio Optimization")
    parser.add_argument("filepath", type=str, help="Path to CSV data file containing asset prices.")
    args = parser.parse_args()

    optimized_portfolios = optimize_portfolio(args.filepath)
    for portfolio in optimized_portfolios:
        print("Weights:", portfolio.x, "Expected Return:", portfolio.fun)
        