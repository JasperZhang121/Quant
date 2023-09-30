import sys
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def arima_forecast(data):
    from statsmodels.tsa.arima.model import ARIMA

    # Fit the ARIMA model
    model = ARIMA(data['Close'], order=(5,1,0))
    model_fit = model.fit()  

    # Forecast
    forecast = model_fit.forecast(steps=5)[0]
    print(f"Next 5 days forecast: {forecast}")


def linear_regression_forecast(data):
    data['Lag1'] = data['Close'].shift(1)
    data.dropna(inplace=True)
    
    X = np.array(data['Lag1']).reshape(-1,1)
    y = data['Close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
    plt.scatter(X_test, y_test, color='blue')
    plt.plot(X_test, predictions, color='red')
    plt.title('Linear Regression Forecast')
    plt.show()

def kmeans_portfolio(data):
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    # Drop rows with NaN values
    data = data.dropna()

    # Normalize the data
    scaler = StandardScaler()
    X = scaler.fit_transform(data)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=2)
    clusters = kmeans.fit_predict(X)
    print(f"Clusters: {clusters}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python model.py <path_to_data_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    data = pd.read_csv(filepath, index_col='Date', parse_dates=True)

    print("\n1. ARIMA Forecast\n")
    arima_forecast(data)

    print("\n2. Linear Regression Forecast\n")
    linear_regression_forecast(data)

    print("\n3. K-Means Clustering for Portfolio Diversification\n")
    kmeans_portfolio(data)