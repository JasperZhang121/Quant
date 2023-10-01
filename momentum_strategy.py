import sys
import pandas as pd

def momentum_strategy(data, window_size=90, hold_period=30):
    """
    Basic Momentum Strategy.
    
    Parameters:
    - data: DataFrame with 'Close' column containing prices.
    - window_size: Lookback period for momentum calculation.
    - hold_period: Period to hold the stock after buying.
    
    Returns:
    - signals: DataFrame containing buy and sell signals.
    """
    
    # Calculate momentum
    data['Momentum'] = data['Close'] - data['Close'].shift(window_size)
    
    # Generate Buy signal when momentum is positive
    data['Buy_Signal'] = (data['Momentum'] > 0).astype(int).shift()
    
    # Generate Sell signal after hold_period days
    data['Sell_Signal'] = data['Buy_Signal'].shift(hold_period)
    
    signals = pd.DataFrame({
        'Date': data.index,
        'Prices': data['Close'],
        'Buy': data['Buy_Signal'],
        'Sell': data['Sell_Signal']
    }).dropna()

    return signals

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: momentum_strategy.py <CSV_DATA_PATH> <WINDOW_SIZE> <HOLD_PERIOD>")
        sys.exit(1)

    filepath = sys.argv[1]
    data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
    window_size = int(sys.argv[2])
    hold_period = int(sys.argv[3])

    signals = momentum_strategy(data, window_size, hold_period)
    print(signals)

    # Save signals to a CSV
    signals.to_csv("analysis_system/data/momentum_signals.csv", index=False)
    print("\nSignals have been saved to 'momentum_signals.csv'")
