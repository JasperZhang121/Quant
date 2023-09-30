# features.py

import pandas as pd
import sys

def generate_features(data):
    # Assuming data is a DataFrame
    
    # 1. Moving Averages
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    # 2. Relative Strength Index (RSI)
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # 3. Bollinger Bands
    data['Bollinger_Middle'] = data['Close'].rolling(window=20).mean()
    data['Bollinger_Upper'] = data['Bollinger_Middle'] + 2*data['Close'].rolling(window=20).std()
    data['Bollinger_Lower'] = data['Bollinger_Middle'] - 2*data['Close'].rolling(window=20).std()

    # 4. Price Change
    data['Price Change'] = data['Close'].diff()

    # 5. Volume Change
    data['Volume Change'] = data['Volume'].diff()

    # Return the data with features, dropping NaN values
    return data.dropna()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: features.py <FILEPATH>")
        sys.exit(1)

    filepath = sys.argv[1]
    data = pd.read_csv(filepath, parse_dates=['Date'], index_col='Date')
    
    data_with_features = generate_features(data)
    
    # Let's say you want to save the data with generated features for now:
    output_filepath = filepath.replace('.csv', '_with_features.csv')
    data_with_features.to_csv(output_filepath)
    print(f"Data with features saved to {output_filepath}")
