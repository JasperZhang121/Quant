import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

def visualize_data(filename):
    # Load data
    data = pd.read_csv(filename, parse_dates=['Date'], index_col='Date')

    # Setting a theme for seaborn
    sns.set_theme()

    # Create a figure and a set of subplots
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 8), sharex=True)

    # Plotting the closing prices
    ax[0].plot(data['Close'], label='Close Price', color='blue')
    ax[0].set_title(f"Closing Prices for {filename.split('_')[1]}")
    ax[0].set_ylabel('Price')

    # Plotting the volume
    ax[1].bar(data.index, data['Volume'], label='Volume', color='gray')
    ax[1].set_title(f"Trading Volume for {filename.split('_')[1]}")
    ax[1].set_ylabel('Volume')

    ticker_symbol = os.path.basename(filename).split('_')[1]
    save_image(fig, ticker_symbol)


    # Display the figure
    plt.tight_layout()
    plt.show()

def save_image(fig, ticker):
    """Save the figure to the images directory under data."""
    image_dir = 'analysis_system/images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)  # create 'images' directory under 'data' if it doesn't exist

    filepath = os.path.join(image_dir, f"{ticker}_visualization.png")

    print("")

    fig.savefig(filepath)
    print(f"Image saved to {filepath}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: visual.py <FILENAME>")
        sys.exit(1)

    filename = sys.argv[1]
    visualize_data(filename)
