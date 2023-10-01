import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tensorflow import keras
from tensorflow.keras import layers

def load_data(filepath):
    """Load and preprocess the data."""
    data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
    return data

def preprocess_data(data, feature_col='Close'):
    """Scale and split the data into training and testing sets."""
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[feature_col].values.reshape(-1, 1))
    
    x, y = [], []
    for i in range(60, len(scaled_data)):
        x.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])
    
    x = np.array(x)
    y = np.array(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    return x_train, x_test, y_train, y_test, scaler

def build_model(input_shape):
    """Build the neural network model."""
    model = keras.Sequential([
        layers.LSTM(units=50, return_sequences=True, input_shape=input_shape),
        layers.Dropout(0.2),
        layers.LSTM(units=50, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(units=50),
        layers.Dropout(0.2),
        layers.Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(model, x_train, y_train, epochs=25, batch_size=32):
    """Train the model."""
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
    return model

def predict(model, x_test, scaler):
    """Make predictions and scale back to original values."""
    y_pred = model.predict(x_test)
    y_pred_transformed = scaler.inverse_transform(y_pred)
    return y_pred_transformed

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python neural_networks.py <data_filepath>")
        sys.exit(1)
        
    filepath = sys.argv[1]
    data = load_data(filepath)
    
    x_train, x_test, y_train, y_test, scaler = preprocess_data(data)
    model = build_model(x_train.shape[1:])
    model = train_model(model, x_train, y_train)
    
    y_pred = predict(model, x_test, scaler)
    
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error for Neural Network: {mse}")