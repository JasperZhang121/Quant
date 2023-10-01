import pandas as pd
import argparse

def mean_reversion_strategy(data, window_size=50, z_threshold=1.0):
    """
    Basic Mean Reversion Strategy.
    
    Parameters:
    - data: DataFrame with 'Close' column containing prices.
    - window_size: Lookback period for moving average calculation.
    - z_threshold: Z-score threshold for buying or selling.
    
    Returns:
    - signals: DataFrame containing buy and sell signals.
    """
    
    # Calculate moving average and standard deviation
    data['Rolling_Mean'] = data['Close'].rolling(window=window_size).mean()
    data['Rolling_Std'] = data['Close'].rolling(window=window_size).std()
    
    # Calculate z-score
    data['Z_Score'] = (data['Close'] - data['Rolling_Mean']) / data['Rolling_Std']
    
    # Generate Buy signal when z-score is below negative threshold
    data['Buy_Signal'] = (data['Z_Score'] < -z_threshold).astype(int)
    
    # Generate Sell signal when z-score is above positive threshold
    data['Sell_Signal'] = (data['Z_Score'] > z_threshold).astype(int)
    
    signals = pd.DataFrame({
        'Date': data.index,
        'Prices': data['Close'],
        'Buy': data['Buy_Signal'],
        'Sell': data['Sell_Signal']
    }).dropna()

    return signals

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mean Reversion Trading Strategy")
    parser.add_argument('filepath', type=str, help="Path to the CSV data file.")
    parser.add_argument('--window_size', type=int, default=50, help="Window size for moving average calculation.")
    parser.add_argument('--z_threshold', type=float, default=1.0, help="Z-score threshold for buying/selling.")
    
    args = parser.parse_args()
    
    data = pd.read_csv(args.filepath, index_col='Date', parse_dates=True)
    
    signals = mean_reversion_strategy(data, args.window_size, args.z_threshold)
    print(signals)

    # Save signals to a CSV
    signals.to_csv("analysis_system/data/mean_reversion_signals.csv", index=False)
    print("\nSignals have been saved to 'mean_reversion_signals.csv'")