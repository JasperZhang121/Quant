import pandas as pd
import sys

def load_data(filename):
    """Load the CSV data into a DataFrame."""
    data = pd.read_csv(filename)
    data['Date'] = pd.to_datetime(data['Date'], utc=True)  # Convert to datetime with timezone
    data['Date'] = data['Date'].dt.tz_convert(None)  # Strip timezone
    data.set_index('Date', inplace=True)
    return data




def drop_duplicates(data):
    """Drop duplicate rows."""
    return data.drop_duplicates()

def fill_missing_values(data):
    """Fill missing values using forward fill method."""
    return data.resample('D').ffill()

def remove_outliers(data, column_name='Close', threshold=3):
    """
    Remove outliers based on the z-score. 
    Data points that deviate by `threshold` times the standard deviation are considered outliers.
    """
    z_scores = (data[column_name] - data[column_name].mean()) / data[column_name].std()
    return data[z_scores.abs() <= threshold]

def ensure_chronological_order(data):
    """Ensure data is in chronological order."""
    return data.sort_index()

def clean_data(data):
    """Clean the dataset by applying all cleaning functions."""

    print(data.head())  # Print the first few rows of the DataFrame
    data = drop_duplicates(data)
    data = fill_missing_values(data)
    print(data.info())


    data = drop_duplicates(data)
    data = fill_missing_values(data)
    data = remove_outliers(data)
    data = ensure_chronological_order(data)
    return data

def save_cleaned_data(data, filename):
    """Save the cleaned data to a CSV."""
    data.to_csv(filename)
    print(f"Cleaned data saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: cleaning.py <INPUT_FILENAME> <OUTPUT_FILENAME>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    data = load_data(input_filename)
    cleaned_data = clean_data(data)
    save_cleaned_data(cleaned_data, output_filename)
